import unittest

from middle_end_course.cfg import ControlFlowGraph


class ControlFlowGraphTests(unittest.TestCase):
    def test_diamond(self) -> None:
        graph = ControlFlowGraph.from_mapping(
            "B0",
            {
                "B0": ["B1", "B2"],
                "B1": ["B3"],
                "B2": ["B3"],
                "B3": [],
                "Dead": [],
            },
        )

        self.assertEqual(graph.reachable(), frozenset({"B0", "B1", "B2", "B3"}))
        self.assertEqual(graph.dominators()["B3"], frozenset({"B0", "B3"}))
        self.assertEqual(
            graph.immediate_dominators(),
            {"B0": None, "B1": "B0", "B2": "B0", "B3": "B0"},
        )
        frontier = graph.dominance_frontier()
        self.assertEqual(frontier["B1"], frozenset({"B3"}))
        self.assertEqual(frontier["B2"], frozenset({"B3"}))
        self.assertEqual(frontier["B0"], frozenset())

    def test_natural_loop_and_self_frontier(self) -> None:
        graph = ControlFlowGraph.from_mapping(
            "B0",
            {
                "B0": ["B1"],
                "B1": ["B2", "B4"],
                "B2": ["B3"],
                "B3": ["B1"],
                "B4": [],
            },
        )
        self.assertEqual(graph.natural_loop("B1", "B3"), frozenset({"B1", "B2", "B3"}))
        frontier = graph.dominance_frontier()
        self.assertEqual(frontier["B1"], frozenset({"B1"}))
        self.assertEqual(frontier["B2"], frozenset({"B1"}))
        self.assertEqual(frontier["B3"], frozenset({"B1"}))

    def test_rejects_unknown_target(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown nodes"):
            ControlFlowGraph.from_mapping("B0", {"B0": ["B1"]})

    def test_rejects_non_back_edge_for_natural_loop(self) -> None:
        graph = ControlFlowGraph.from_mapping("B0", {"B0": ["B1"], "B1": []})
        with self.assertRaisesRegex(ValueError, "not an edge"):
            graph.natural_loop("B0", "B1")


if __name__ == "__main__":
    unittest.main()
