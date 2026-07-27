from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .analysis import (
    analyze_dominators,
    analyze_natural_loop,
    compute_dominance_frontier,
    compute_immediate_dominators,
)
from .cfg import ControlFlowGraph


COMMANDS = {"summary", "dominators", "natural-loop"}


def _load_graph(path: Path) -> ControlFlowGraph:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON root must be an object")
    entry = payload.get("entry")
    successors = payload.get("successors")
    if not isinstance(entry, str) or not entry:
        raise ValueError("field 'entry' must be a non-empty string")
    if not isinstance(successors, dict):
        raise ValueError("field 'successors' must be an object")

    normalized: dict[str, list[str]] = {}
    for node, targets in successors.items():
        if not isinstance(node, str) or not node:
            raise ValueError("successor-map keys must be non-empty strings")
        if not isinstance(targets, list) or any(
            not isinstance(target, str) or not target for target in targets
        ):
            raise ValueError(f"successors[{node!r}] must be a list of strings")
        normalized[node] = targets
    return ControlFlowGraph.from_mapping(entry, normalized)


def _sets_to_json(values: Any) -> Any:
    if isinstance(values, dict):
        return {key: _sets_to_json(value) for key, value in values.items()}
    if hasattr(values, "items"):
        return {key: _sets_to_json(value) for key, value in values.items()}
    if isinstance(values, list):
        return [_sets_to_json(value) for value in values]
    if isinstance(values, tuple):
        return [_sets_to_json(value) for value in values]
    if isinstance(values, (set, frozenset)):
        return [_sets_to_json(value) for value in sorted(values)]
    return values


def _print_json(payload: Any) -> None:
    print(json.dumps(_sets_to_json(payload), ensure_ascii=False, indent=2, sort_keys=True))


def _print_dominator_trace(graph: ControlFlowGraph) -> None:
    analysis = analyze_dominators(graph)
    for iteration in analysis.iterations:
        changed = ", ".join(iteration.changed_nodes) or "—"
        print(f"iteration {iteration.index}; changed: {changed}")
        for node, values in iteration.dominators.items():
            print(f"  Dom({node}) = {{{', '.join(sorted(values))}}}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect a small teaching control-flow graph"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    summary = subparsers.add_parser("summary", help="print all final analyses")
    summary.add_argument("graph", type=Path)

    dominators = subparsers.add_parser(
        "dominators", help="compute dominators, optionally with every iteration"
    )
    dominators.add_argument("graph", type=Path)
    dominators.add_argument("--trace", action="store_true")
    dominators.add_argument("--format", choices=("human", "json"), default="human")

    natural_loop = subparsers.add_parser(
        "natural-loop", help="collect a natural loop for a proven back edge"
    )
    natural_loop.add_argument("graph", type=Path)
    natural_loop.add_argument("--header", required=True)
    natural_loop.add_argument("--latch", required=True)
    natural_loop.add_argument("--trace", action="store_true")
    natural_loop.add_argument("--format", choices=("human", "json"), default="human")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args_list = list(sys.argv[1:] if argv is None else argv)
    # Backward compatibility with the original `course-cfg graph.json` command.
    if args_list and args_list[0] not in COMMANDS and not args_list[0].startswith("-"):
        args_list.insert(0, "summary")

    parser = build_parser()
    args = parser.parse_args(args_list)

    try:
        graph = _load_graph(args.graph)
        if args.command == "summary":
            dominators = analyze_dominators(graph).dominators
            _print_json(
                {
                    "reachable": graph.reachable(),
                    "predecessors": graph.predecessors(),
                    "dominators": dominators,
                    "immediate_dominators": compute_immediate_dominators(
                        graph, dominators
                    ),
                    "dominance_frontier": compute_dominance_frontier(
                        graph, dominators
                    ),
                }
            )
            return 0

        if args.command == "dominators":
            analysis = analyze_dominators(graph)
            if args.format == "json":
                _print_json(
                    {
                        "dominators": analysis.dominators,
                        "iterations": [
                            {
                                "index": item.index,
                                "changed_nodes": item.changed_nodes,
                                "dominators": item.dominators,
                            }
                            for item in analysis.iterations
                        ]
                        if args.trace
                        else [],
                    }
                )
            elif args.trace:
                _print_dominator_trace(graph)
            else:
                for node, values in analysis.dominators.items():
                    print(f"Dom({node}) = {{{', '.join(sorted(values))}}}")
            return 0

        loop = analyze_natural_loop(
            graph, header=args.header, latch=args.latch
        )
        if args.format == "json":
            _print_json(
                {
                    "header": loop.header,
                    "latch": loop.latch,
                    "nodes": loop.nodes,
                    "steps": [
                        {
                            "popped": item.popped,
                            "considered_predecessors": item.considered_predecessors,
                            "added_nodes": item.added_nodes,
                            "loop_after_step": item.loop_after_step,
                        }
                        for item in loop.steps
                    ]
                    if args.trace
                    else [],
                }
            )
        else:
            print(f"natural loop: {{{', '.join(sorted(loop.nodes))}}}")
            if args.trace:
                for index, step in enumerate(loop.steps, start=1):
                    print(
                        f"step {index}: pop {step.popped}; "
                        f"pred={list(step.considered_predecessors)}; "
                        f"add={list(step.added_nodes)}; "
                        f"loop={sorted(step.loop_after_step)}"
                    )
        return 0
    except ValueError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover; argparse exits


if __name__ == "__main__":
    raise SystemExit(main())
