from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from middle_end_course.cli import main


class CliTests(unittest.TestCase):
    def graph_file(self, payload: object) -> tempfile.TemporaryDirectory[str]:
        raise NotImplementedError

    def run_with_graph(self, args: list[str], payload: object) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graph.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main([*args, str(path)])
            return code, output.getvalue()

    def test_summary_backward_compatible(self) -> None:
        code, output = self.run_with_graph([], {"entry": "A", "successors": {"A": []}})
        self.assertEqual(code, 0)
        self.assertIn('"reachable"', output)

    def test_dominator_human_trace(self) -> None:
        code, output = self.run_with_graph(
            ["dominators", "--trace"],
            {"entry": "A", "successors": {"A": ["B"], "B": []}},
        )
        self.assertEqual(code, 0)
        self.assertIn("iteration 0", output)
        self.assertIn("Dom(B)", output)

    def test_dominator_json_trace(self) -> None:
        code, output = self.run_with_graph(
            ["dominators", "--trace", "--format", "json"],
            {"entry": "A", "successors": {"A": []}},
        )
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(output)["iterations"])

    def test_natural_loop_human_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graph.json"
            path.write_text(json.dumps({"entry": "E", "successors": {"E": ["H"], "H": ["L", "X"], "L": ["H"], "X": []}}), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["natural-loop", str(path), "--header", "H", "--latch", "L", "--trace"])
            self.assertEqual(code, 0)
            self.assertIn("natural loop", output.getvalue())
            self.assertIn("step 1", output.getvalue())


if __name__ == "__main__":
    unittest.main()
