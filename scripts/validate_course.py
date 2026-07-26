from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED = [
    ROOT / "README.md",
    ROOT / "mkdocs.yml",
    DOCS / "index.md",
    DOCS / "course-map.md",
    DOCS / "ir-contract.md",
    DOCS / "practice/answers-and-rubrics.md",
]

LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_SRC_PATTERN = re.compile(r"<(?:img|a)\b[^>]*(?:src|href)=['\"]([^'\"]+)['\"]", re.I)
FORBIDDEN = [
    "/mnt/data/",
    "../assets/diagrams/",
    "Что прислать мне",
    "Когда обращаться ко мне",
    "У Дмитрия",
    "у Дмитрия",
    "Работа со мной",
    "статья Дмитрия",
    "статьи Дмитрия",
    "3–9 августа",
    "15–24 июля",
    "Резерв: 2–6 августа",
]


def validate_links(path: Path, text: str, errors: list[str]) -> None:
    links = LINK_PATTERN.findall(text) + HTML_SRC_PATTERN.findall(text)
    for link in links:
        target = link.strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: missing local target {link}")


def main() -> int:
    errors: list[str] = []
    for path in REQUIRED:
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    modules = sorted((DOCS / "modules").glob("*.md"))
    if len(modules) != 20:
        errors.append(f"expected 20 modules, found {len(modules)}")

    for index, path in enumerate(modules, start=1):
        text = path.read_text(encoding="utf-8")
        if not text.startswith(f"# Занятие {index}."):
            errors.append(f"{path.relative_to(ROOT)}: incorrect top-level title")
        for marker in ("Сначала простыми словами", "Обязательная практика", "Три вопроса", "```mermaid"):
            if marker not in text:
                errors.append(f"{path.relative_to(ROOT)}: missing section {marker!r}")

    for path in [ROOT / "README.md", *DOCS.rglob("*.md")]:
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN:
            if forbidden in text:
                errors.append(f"{path.relative_to(ROOT)}: forbidden source-specific text {forbidden!r}")
        validate_links(path, text, errors)

    if errors:
        print("Course validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Course validation passed: {len(modules)} modules and all local links resolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
