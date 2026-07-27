from __future__ import annotations

import re
import sys
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MODULES = DOCS / "modules"

EXPECTED_MODULES = [
    "01-pipeline-and-diagnostic.md",
    "02-leaders-and-basic-blocks.md",
    "03-building-cfg.md",
    "04-dominators.md",
    "05-idom-tree-and-df.md",
    "06-ssa-and-phi.md",
    "07-ssa-renaming.md",
    "08-dependencies-and-lvn.md",
    "09-constants.md",
    "10-dce-uce-and-pass-order.md",
    "11-inlining.md",
    "12-checkpoint-1.md",
    "13-loop-concepts.md",
    "14-havlak-and-loop-tree.md",
    "15-induction-variables.md",
    "16-licm.md",
    "17-loop-transformations.md",
    "18-checkpoint-2.md",
    "19-mock-exam-1.md",
    "20-final-repair.md",
]

REQUIRED_SECTIONS = [
    "## Зачем это вообще нужно",
    "## Термины до заданий",
    "## Ключевая схема",
    "## Пошаговый разбор",
    "## Формальное правило",
    "## Типичные ошибки",
    "## Задача A — по образцу",
    "## Самостоятельная задача",
    "## Проверь себя",
    "## Как это устроено в промышленном компиляторе",
]

OBSOLETE_SECTIONS = [
    "## Первая модель",
    "## Разобранный пример: состояние за состоянием",
    "## Задача B — перенос на новый пример",
    "## Проверка на выходе",
    "## Профессиональная граница",
]

FORBIDDEN_EDITORIAL_PHRASES = [
    "prerequisite bridges",
    "worked trace",
    "transfer example",
    "cleanup pipeline",
    "legality matrix",
    "preheader repair",
    "name, type and effect analysis",
    "cfg rewrite",
    "loop pipeline",
    "optional extension",
    "production implementation",
    "middle-end foundations",
    "human/json",
    "inner-loop child of outer-loop",
]

ALLOWED_ENGLISH_WORDS = {
    "AST",
    "BFS",
    "CFG",
    "CIL",
    "DCE",
    "DF",
    "DFS",
    "GitHub",
    "IDom",
    "IR",
    "JSON",
    "LCSSA",
    "LICM",
    "LLVM",
    "LVN",
    "MemorySSA",
    "MkDocs",
    "NaN",
    "Python",
    "SCC",
    "SCCP",
    "SSA",
    "UCE",
}

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TERM_ROW_RE = re.compile(
    r"^\| \*\*(.+?)\*\*(?: \(\*.+?\*\))? \| (.+?) \| (.+?) \|$"
)
ENGLISH_WORD_RE = re.compile(r"(?<![А-Яа-яЁё])([A-Za-z][A-Za-z-]*)(?![А-Яа-яЁё])")
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9-]+")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_link(path: Path, raw_target: str, errors: list[str]) -> None:
    target = raw_target.split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return
    resolved = (path.parent / target).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        fail(errors, f"{path.relative_to(ROOT)}: link escapes repository: {raw_target}")
        return
    if not resolved.exists():
        fail(errors, f"{path.relative_to(ROOT)}: broken link: {raw_target}")


def iter_prose_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield prose lines, excluding code, term tables, links and English aliases."""

    in_code = False
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or stripped.startswith("|"):
            continue
        if re.fullmatch(r"</?(?:details|summary)>.*", stripped):
            continue

        line = re.sub(r"<[^>]+>", "", raw_line)
        line = re.sub(r"`[^`]*`", "", line)
        line = re.sub(r"https?://\S+", "", line)
        line = re.sub(r"\[[^\]]+\]\([^)]*\)", "", line)
        # English aliases are allowed once, immediately after a Russian term.
        line = re.sub(r"\([^)]*[A-Za-z][^)]*\)", "", line)
        if line.strip():
            yield line_number, line


def check_editorial_style(path: Path, text: str, errors: list[str]) -> None:
    for line_number, line in iter_prose_lines(text):
        lowered = line.casefold()
        for phrase in FORBIDDEN_EDITORIAL_PHRASES:
            if phrase in lowered:
                fail(
                    errors,
                    f"{path.name}:{line_number}: mixed-language phrase remains: {phrase!r}",
                )

        english_words = [
            word
            for word in ENGLISH_WORD_RE.findall(line)
            if word not in ALLOWED_ENGLISH_WORDS
            and not (len(word) <= 4 and word.isupper())
        ]
        if len(english_words) >= 4:
            fail(
                errors,
                f"{path.name}:{line_number}: too many unexplained English words "
                f"in prose: {english_words}",
            )

        word_count = len(WORD_RE.findall(line))
        if word_count > 55:
            fail(
                errors,
                f"{path.name}:{line_number}: sentence/paragraph is too dense "
                f"({word_count} words)",
            )


def validate_module(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            fail(errors, f"{path.name}: missing section {section!r}")

    positions = [text.find(section) for section in REQUIRED_SECTIONS]
    if positions != sorted(positions):
        fail(errors, f"{path.name}: required teaching sections are out of order")

    for section in OBSOLETE_SECTIONS:
        if section in text:
            fail(errors, f"{path.name}: obsolete editorial heading remains: {section!r}")

    if "<table" in text.lower() or "<tbody" in text.lower():
        fail(errors, f"{path.name}: conversion HTML table remains")

    task_pos = text.find("## Задача A — по образцу")
    terms_pos = text.find("## Термины до заданий")
    if not (0 <= terms_pos < task_pos):
        fail(errors, f"{path.name}: terms must be explained before task A")

    term_rows = [TERM_ROW_RE.match(line) for line in text.splitlines()]
    term_rows = [match for match in term_rows if match]
    if len(term_rows) != 5:
        fail(errors, f"{path.name}: expected exactly 5 defined terms, got {len(term_rows)}")
    for match in term_rows:
        assert match is not None
        if not match.group(2).strip() or not match.group(3).strip():
            fail(errors, f"{path.name}: empty term definition for {match.group(1)!r}")

    if text.count("<details>") < 3:
        fail(errors, f"{path.name}: task/self-check answers are not locally available")
    if "Моя формулировка одним предложением" in text:
        fail(errors, f"{path.name}: empty self-definition table returned")

    check_editorial_style(path, text, errors)

    for link in LINK_RE.findall(text):
        check_link(path, link, errors)


def main() -> int:
    errors: list[str] = []

    actual_modules = sorted(path.name for path in MODULES.glob("*.md"))
    if actual_modules != EXPECTED_MODULES:
        fail(errors, f"module inventory mismatch: {actual_modules}")

    for name in EXPECTED_MODULES:
        validate_module(MODULES / name, errors)

    for path in DOCS.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for link in LINK_RE.findall(text):
            check_link(path, link, errors)

    for path in [ROOT / "README.md", DOCS / "index.md", DOCS / "course-map.md"]:
        check_editorial_style(path, path.read_text(encoding="utf-8"), errors)

    glossary = (DOCS / "resources" / "glossary.md").read_text(encoding="utf-8")
    if "см. точное определение" in glossary.lower():
        fail(errors, "glossary contains placeholder definitions")
    glossary_names = re.findall(
        r"^\| \*\*(.+?)\*\*", glossary, flags=re.MULTILINE
    )
    glossary_terms = len(glossary_names)
    if glossary_terms != 100:
        fail(errors, f"glossary must contain exactly 100 rows, got {glossary_terms}")
    if len(set(glossary_names)) != glossary_terms:
        fail(errors, "glossary contains duplicate Russian term names")

    prerequisite = (DOCS / "prerequisites.md").read_text(encoding="utf-8")
    for phrase in [
        "Привязка имени, хранилище и значение",
        "DFS",
        "SCC",
        "Межитерационная зависимость",
    ]:
        if phrase not in prerequisite:
            fail(errors, f"prerequisites missing {phrase!r}")

    lesson1 = (MODULES / EXPECTED_MODULES[0]).read_text(encoding="utf-8")
    for phrase in ["анализ имён", "анализ типов", "анализ эффектов"]:
        if lesson1.find(phrase) == -1 or lesson1.find(phrase) > lesson1.find("## Задача A"):
            fail(errors, f"lesson 1 does not explain {phrase!r} before tasks")

    lesson9 = (MODULES / EXPECTED_MODULES[8]).read_text(encoding="utf-8")
    if "SCCP не требуется для обязательной части" not in lesson9:
        fail(errors, "lesson 9 does not separate simple propagation from optional SCCP")

    lesson18 = (MODULES / EXPECTED_MODULES[17]).read_text(encoding="utf-8")
    if "первые 120 минут работа выполняется без подсказок" not in lesson18:
        fail(errors, "lesson 18 control-mode help rule is not explicit")

    lesson19 = (MODULES / EXPECTED_MODULES[18]).read_text(encoding="utf-8")
    if lesson19.find("Теоретический билет — 7 вопросов") > lesson19.find("## Задача A"):
        fail(errors, "lesson 19 ticket appears after the task that references it")

    lesson20 = (MODULES / EXPECTED_MODULES[19]).read_text(encoding="utf-8")
    if "../practice/transfer-bank.md" not in lesson20:
        fail(errors, "lesson 20 is not autonomous: transfer bank link missing")

    forbidden = [
        "который я дам в нашей сессии",
        "Финальный занятие",
        "Последний занятие",
        "Name, type and effect analysis]",
    ]
    all_active = "\n".join(
        (MODULES / name).read_text(encoding="utf-8") for name in EXPECTED_MODULES
    )
    for phrase in forbidden:
        if phrase in all_active:
            fail(errors, f"forbidden pedagogical/conversion phrase remains: {phrase!r}")

    if errors:
        print("Course validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Course validation passed: {len(EXPECTED_MODULES)} modules, "
        f"{glossary_terms} glossary terms, local answers, prerequisite and "
        "readability checks."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
