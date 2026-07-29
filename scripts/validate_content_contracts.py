from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


REQUIRED_PHRASES: dict[str, list[str]] = {
    "docs/ir-contract.md": [
        "Контракт учебного IR v1",
        "Нормализованный CFG-IR",
        "обёртыванием по модулю `2^32`",
        "используется единая запись `x3 = φ[B1: x1, B2: x2]`",
        "Если контракт вызова не указан, используется `unknown`.",
    ],
    "docs/modules/02-leaders-and-basic-blocks.md": [
        "при нормализации в конец `B2` добавляется `jump B3`",
        "каждый блок имеет ровно один терминатор",
    ],
    "docs/modules/03-building-cfg.md": [
        "Соседство уже было учтено на этапе нормализации",
    ],
    "docs/modules/12-checkpoint-1.md": [
        "Полный эталон задачи A",
        "DF(B1) = {B3}",
        "Итоговый наблюдаемый результат: `print 8`.",
    ],
    "docs/modules/13-loop-concepts.md": [
        "не менее двух различных входных вершин",
        "два внешних ребра, оба ведущие только в `A`, ещё не доказывают несводимость",
    ],
    "docs/modules/14-havlak-and-loop-tree.md": [
        "Полная самостоятельная реализация конкретного варианта алгоритма",
        "Это **не полный псевдокод Хавлака**.",
    ],
    "docs/modules/18-checkpoint-2.md": [
        "body:",
        "latch:",
        "Полный эталон задачи A",
        "DF(BODY) = {H}",
        "Это глобальное устранение общего выражения или распространение доминирующего значения, а не LVN",
    ],
}

FORBIDDEN_PHRASES: dict[str, list[str]] = {
    "docs/modules/14-havlak-and-loop-tree.md": [
        "Полный пошаговый разбор на небольшом графе вместо списка загадочных названий",
    ],
    "docs/modules/18-checkpoint-2.md": [
        "Замыкающий блок обновляет `i`, а тело — `s`",
    ],
}


def main() -> int:
    errors: list[str] = []

    for relative, phrases in REQUIRED_PHRASES.items():
        path = ROOT / relative
        if not path.exists():
            errors.append(f"missing required file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{relative}: missing required content marker {phrase!r}")

    for relative, phrases in FORBIDDEN_PHRASES.items():
        path = ROOT / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase in text:
                errors.append(f"{relative}: obsolete or contradictory phrase remains {phrase!r}")

    golden = ROOT / "examples" / "course-golden.json"
    semantic_validator = ROOT / "scripts" / "validate_golden_examples.py"
    if not golden.exists() or not semantic_validator.exists():
        errors.append("semantic golden validation files are incomplete")

    if errors:
        print("Content contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Content contract validation passed: deterministic IR, normalized CFG, "
        "irreducibility, Havlak scope and complete checkpoint markers."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
