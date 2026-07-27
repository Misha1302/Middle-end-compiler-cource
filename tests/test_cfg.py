from __future__ import annotations

import unittest
from types import MappingProxyType

from middle_end_course import (
    ControlFlowGraph,
    analyze_dominators,
    analyze_natural_loop,
    compute_dominance_frontier,
    compute_immediate_dominators,
)


class ControlFlowGraphTests(unittest.TestCase):
    def diamond(self) -> ControlFlowGraph:
        return ControlFlowGraph.from_mapping(
            "B0", {"B0": ["B1", "B2"], "B1": ["B3"], "B2": ["B3"], "B3": []}
        )

    def test_reachable_excludes_dead(self) -> None:
        g = ControlFlowGraph.from_mapping("E", {"E": ["X"], "X": [], "D": []})
        self.assertEqual(g.reachable(), frozenset({"E", "X"}))

    def test_predecessors_are_sorted_and_read_only(self) -> None:
        g = ControlFlowGraph.from_mapping("A", {"A": ["C", "B"], "B": ["C"], "C": []})
        self.assertEqual(g.predecessors()["C"], ("A", "B"))
        self.assertIsInstance(g.predecessors(), MappingProxyType)

    def test_input_is_copied(self) -> None:
        source = {"A": ["B"], "B": []}
        g = ControlFlowGraph.from_mapping("A", source)
        source["A"].append("A")
        self.assertEqual(g.successors["A"], ("B",))

    def test_successors_are_read_only(self) -> None:
        g = self.diamond()
        with self.assertRaises(TypeError):
            g.successors["B0"] = ()  # type: ignore[index]

    def test_rejects_empty_entry(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-empty"):
            ControlFlowGraph.from_mapping("", {"A": []})

    def test_rejects_unknown_target(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown nodes"):
            ControlFlowGraph.from_mapping("A", {"A": ["B"]})

    def test_rejects_duplicate_successor(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate"):
            ControlFlowGraph.from_mapping("A", {"A": ["B", "B"], "B": []})

    def test_dominator_result_for_diamond(self) -> None:
        result = analyze_dominators(self.diamond()).dominators
        self.assertEqual(result["B3"], frozenset({"B0", "B3"}))

    def test_dominator_trace_starts_with_maximal_sets(self) -> None:
        trace = analyze_dominators(self.diamond()).iterations
        self.assertEqual(trace[0].dominators["B1"], frozenset({"B0", "B1", "B2", "B3"}))
        self.assertEqual(trace[-1].changed_nodes, ())

    def test_immediate_dominators(self) -> None:
        self.assertEqual(
            dict(compute_immediate_dominators(self.diamond())),
            {"B0": None, "B1": "B0", "B2": "B0", "B3": "B0"},
        )

    def test_dominance_frontier_for_diamond(self) -> None:
        df = compute_dominance_frontier(self.diamond())
        self.assertEqual(df["B1"], frozenset({"B3"}))
        self.assertEqual(df["B2"], frozenset({"B3"}))

    def test_natural_loop_trace(self) -> None:
        g = ControlFlowGraph.from_mapping(
            "E", {"E": ["H"], "H": ["B", "X"], "B": ["L"], "L": ["H"], "X": []}
        )
        result = analyze_natural_loop(g, header="H", latch="L")
        self.assertEqual(result.nodes, frozenset({"H", "B", "L"}))
        self.assertTrue(result.steps)
        self.assertEqual(result.steps[0].popped, "L")

    def test_self_loop_does_not_capture_preheader(self) -> None:
        g = ControlFlowGraph.from_mapping("E", {"E": ["H"], "H": ["H", "X"], "X": []})
        self.assertEqual(g.natural_loop("H", "H"), frozenset({"H"}))

    def test_loop_ignores_unreachable_predecessor(self) -> None:
        g = ControlFlowGraph.from_mapping(
            "E", {"E": ["H"], "H": ["B", "X"], "B": ["L"], "L": ["H"], "X": [], "D": ["B"]}
        )
        self.assertNotIn("D", g.natural_loop("H", "L"))

    def test_rejects_non_edge_as_back_edge(self) -> None:
        with self.assertRaisesRegex(ValueError, "not an edge"):
            self.diamond().natural_loop("B0", "B1")

    def test_rejects_edge_without_dominance(self) -> None:
        g = ControlFlowGraph.from_mapping("E", {"E": ["A", "B"], "A": ["B"], "B": ["A"]})
        with self.assertRaisesRegex(ValueError, "does not dominate"):
            g.natural_loop("A", "B")

    def test_rejects_unreachable_loop(self) -> None:
        g = ControlFlowGraph.from_mapping("E", {"E": [], "D": ["D"]})
        with self.assertRaisesRegex(ValueError, "reachable"):
            g.natural_loop("D", "D")


if __name__ == "__main__":
    unittest.main()
