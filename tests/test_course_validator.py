from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "course_validator", ROOT / "scripts/validate_course.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load course validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class CourseValidatorTests(unittest.TestCase):
    def test_repository_link_is_accepted(self) -> None:
        errors: list[str] = []
        VALIDATOR.check_link(ROOT / "docs/index.md", "course-map.md", errors)
        self.assertEqual(errors, [])

    def test_escaping_link_is_rejected(self) -> None:
        errors: list[str] = []
        VALIDATOR.check_link(
            ROOT / "docs/index.md", "../../../../etc/passwd", errors
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("escapes repository", errors[0])


if __name__ == "__main__":
    unittest.main()
