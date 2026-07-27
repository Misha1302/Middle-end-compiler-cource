from __future__ import annotations

import re
import sys
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
    "## Первая модель",
    "## Разобранный пример: состояние за состоянием",
    "## Формальное правило",
    "## Типичные ошибки",
    "## Задача A — по образцу",
    "## Задача B — перенос на новый пример",
    "## Проверка на выходе",
]

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TERM_ROW_RE = re.compile(r"^\| \*\*(.+?)\*\* \| (.+?) \| (.+?) \|$")


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


def validate_module(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            fail(errors, f"{path.name}: missing section {section!r}")

    positions = [text.find(section) for section in REQUIRED_SECTIONS]
    if positions != sorted(positions):
        fail(errors, f"{path.name}: required teaching sections are out of order")

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
        fail(errors, f"{path.name}: task/exit answers are not locally available")
    if "Моя формулировка одним предложением" in text:
        fail(errors, f"{path.name}: empty self-definition table returned")

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

    glossary = (DOCS / "resources" / "glossary.md").read_text(encoding="utf-8")
    if "см. точное определение" in glossary.lower():
        fail(errors, "glossary contains placeholder definitions")
    glossary_terms = len(re.findall(r"^\| \*\*.+?\*\* \|", glossary, flags=re.MULTILINE))
    if glossary_terms < 100:
        fail(errors, f"glossary is incomplete: only {glossary_terms} terms")

    prerequisite = (DOCS / "prerequisites.md").read_text(encoding="utf-8")
    for phrase in ["Binding, storage и value", "DFS", "SCC", "Loop-carried dependence"]:
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
        "Name, type and effect analysis]",  # untranslated diagram label
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
        f"{glossary_terms} glossary terms, local answers and prerequisite checks."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
