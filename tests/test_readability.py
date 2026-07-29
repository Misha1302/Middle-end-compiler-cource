from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_readability import analyze_file


class ReadabilityCheckTests(unittest.TestCase):
    def write_markdown(self, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "sample.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_reports_long_prose_sentence(self) -> None:
        words = " ".join(f"слово{index}" for index in range(37))
        path = self.write_markdown(f"# Заголовок\n\n{words}.\n")

        findings = analyze_file(path)

        self.assertEqual(1, len(findings))
        self.assertEqual("long sentence", findings[0].kind)
        self.assertEqual(37, findings[0].value)

    def test_reports_long_numbered_item(self) -> None:
        words = " ".join(f"слово{index}" for index in range(37))
        path = self.write_markdown(f"1. {words}.\n")

        findings = analyze_file(path)

        self.assertEqual(1, len(findings))
        self.assertEqual("long sentence", findings[0].kind)

    def test_reports_inflected_abstract_terms(self) -> None:
        path = self.write_markdown(
            "Анализы алгоритма требуют доказательства допустимости "
            "преобразования и проверки инварианта.\n"
        )

        findings = analyze_file(path)

        self.assertEqual(1, len(findings))
        self.assertEqual("abstract-term density", findings[0].kind)
        self.assertEqual(6, findings[0].value)

    def test_ignores_code_and_tables(self) -> None:
        words = " ".join(f"word{index}" for index in range(50))
        path = self.write_markdown(
            "# Заголовок\n\n"
            f"| {words} |\n\n"
            "```text\n"
            f"{words}\n"
            "```\n"
        )

        self.assertEqual([], analyze_file(path))


if __name__ == "__main__":
    unittest.main()
