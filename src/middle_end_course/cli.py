from __future__ import annotations

import argparse
import json
from pathlib import Path

from .cfg import ControlFlowGraph


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a teaching CFG from JSON")
    parser.add_argument("graph", type=Path, help="JSON file with entry and successors")
    parser.add_argument("--loop", nargs=2, metavar=("HEADER", "LATCH"))
    args = parser.parse_args()

    payload = json.loads(args.graph.read_text(encoding="utf-8"))
    graph = ControlFlowGraph.from_mapping(payload["entry"], payload["successors"])
    result: dict[str, object] = {
        "reachable": sorted(graph.reachable()),
        "predecessors": {k: list(v) for k, v in graph.predecessors().items()},
        "dominators": {k: sorted(v) for k, v in graph.dominators().items()},
        "immediate_dominators": graph.immediate_dominators(),
        "dominance_frontier": {
            k: sorted(v) for k, v in graph.dominance_frontier().items()
        },
    }
    if args.loop:
        result["natural_loop"] = sorted(graph.natural_loop(*args.loop))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
