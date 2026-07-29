from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# These pages form the entry path or contain the densest explanations. They
# use a hard limit; the rest of the course is reported so it can be improved
# gradually without blocking unrelated changes.
STRICT_FILES = {
    Path("docs/getting-started.md"),
    Path("docs/ir-contract.md"),
    Path("docs/modules/11-inlining.md"),
    Path("docs/modules/14-havlak-and-loop-tree.md"),
}

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+(?:[-–—][A-Za-zА-Яа-яЁё0-9]+)*")
SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+")
LIST_PREFIX_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
ABSTRACT_STEMS = (
    "анализ",
    "алгоритм",
    "доказ",
    "допустим",
    "инвариант",
    "контракт",
    "област",
    "оптимизац",
    "представител",
    "преобразован",
    "реализац",
    "семантик",
    "состояни",
)


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    kind: str
    value: int
    text: str


def iter_prose_lines(path: Path) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    in_code = False

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped:
            continue
        if stripped.startswith(("|", "#", "<")):
            continue

        line = LIST_PREFIX_RE.sub("", raw_line)
        line = re.sub(r"^\s*>\s?", "", line)
        line = re.sub(r"`[^`]*`", " термин ", line)
        line = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", line)
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\*\*|__|\*|_", "", line)
        if line.strip():
            lines.append((line_number, line.strip()))

    return lines


def abstract_stem_count(words: list[str]) -> int:
    lowered = {word.casefold() for word in words}
    return sum(any(word.startswith(stem) for word in lowered) for stem in ABSTRACT_STEMS)


def analyze_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []

    for line_number, line in iter_prose_lines(path):
        for sentence in SENTENCE_END_RE.split(line):
            sentence = sentence.strip()
            if not sentence:
                continue

            words = WORD_RE.findall(sentence)
            if len(words) > 36:
                findings.append(
                    Finding(path, line_number, "long sentence", len(words), sentence)
                )

            abstract_count = abstract_stem_count(words)
            if abstract_count >= 6:
                findings.append(
                    Finding(
                        path,
                        line_number,
                        "abstract-term density",
                        abstract_count,
                        sentence,
                    )
                )

    return findings


def relative(path: Path) -> Path:
    return path.relative_to(ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report dense Russian prose in the course documentation."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail when a finding appears in one of the protected high-impact pages",
    )
    args = parser.parse_args()

    findings: list[Finding] = []
    for path in sorted(DOCS.rglob("*.md")):
        findings.extend(analyze_file(path))

    strict_findings = [item for item in findings if relative(item.path) in STRICT_FILES]

    if findings:
        print(f"Readability report: {len(findings)} dense sentence(s).")
        for item in findings[:40]:
            rel = relative(item.path)
            print(
                f"- {rel}:{item.line}: {item.kind}={item.value}: "
                f"{item.text[:180]}"
            )
        if len(findings) > 40:
            print(f"- ... {len(findings) - 40} more finding(s)")
    else:
        print("Readability report: no dense prose found.")

    if args.strict and strict_findings:
        print("Strict readability validation failed for protected pages.")
        return 1

    if args.strict:
        print("Strict readability validation passed for protected pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
