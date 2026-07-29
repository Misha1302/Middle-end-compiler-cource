from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GOLDEN_PATH = ROOT / "examples" / "course-golden.json"


def normalize(mapping: dict[str, set[str]]) -> dict[str, list[str]]:
    return {key: sorted(value) for key, value in sorted(mapping.items())}


def reachable(entry: str, succ: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    queue: deque[str] = deque([entry])
    while queue:
        node = queue.popleft()
        if node in seen:
            continue
        seen.add(node)
        queue.extend(sorted(succ[node] - seen))
    return seen


def compute_dominators(
    entry: str,
    vertices: set[str],
    pred: dict[str, set[str]],
) -> dict[str, set[str]]:
    dom = {vertex: set(vertices) for vertex in vertices}
    dom[entry] = {entry}

    changed = True
    while changed:
        changed = False
        for vertex in sorted(vertices - {entry}):
            predecessors = pred[vertex]
            if not predecessors:
                raise ValueError(f"reachable non-entry vertex has no predecessor: {vertex}")
            common = set(vertices)
            for predecessor in predecessors:
                common &= dom[predecessor]
            updated = {vertex} | common
            if updated != dom[vertex]:
                dom[vertex] = updated
                changed = True
    return dom


def compute_idom(
    entry: str,
    vertices: set[str],
    dom: dict[str, set[str]],
) -> dict[str, str]:
    result: dict[str, str] = {}
    for vertex in sorted(vertices - {entry}):
        strict = dom[vertex] - {vertex}
        candidates = [
            candidate
            for candidate in strict
            if all(other == candidate or other in dom[candidate] for other in strict)
        ]
        if len(candidates) != 1:
            raise ValueError(
                f"expected one immediate dominator for {vertex}, got {sorted(candidates)}"
            )
        result[vertex] = candidates[0]
    return result


def compute_frontier(
    vertices: set[str],
    pred: dict[str, set[str]],
    dom: dict[str, set[str]],
) -> dict[str, set[str]]:
    frontier = {vertex: set() for vertex in vertices}
    for x in vertices:
        for y in vertices:
            x_strictly_dominates_y = x != y and x in dom[y]
            if x_strictly_dominates_y:
                continue
            if any(x in dom[predecessor] for predecessor in pred[y]):
                frontier[x].add(y)
    return frontier


def validate_example(example: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    example_id = str(example["id"])
    entry = str(example["entry"])
    edges = [(str(source), str(target)) for source, target in example["edges"]]

    expected_dom = {
        str(vertex): {str(item) for item in values}
        for vertex, values in example["dominators"].items()
    }
    vertices = set(expected_dom)
    if entry not in vertices:
        return [f"{example_id}: entry {entry!r} is absent from dominator table"]

    succ: dict[str, set[str]] = defaultdict(set)
    pred: dict[str, set[str]] = defaultdict(set)
    for vertex in vertices:
        succ[vertex]
        pred[vertex]
    for source, target in edges:
        if source not in vertices or target not in vertices:
            errors.append(
                f"{example_id}: edge {source}->{target} references an unknown vertex"
            )
            continue
        succ[source].add(target)
        pred[target].add(source)

    if errors:
        return errors

    actual_reachable = reachable(entry, succ)
    if actual_reachable != vertices:
        errors.append(
            f"{example_id}: expected every listed vertex to be reachable; "
            f"reachable={sorted(actual_reachable)}, vertices={sorted(vertices)}"
        )
        return errors

    actual_dom = compute_dominators(entry, vertices, pred)
    if normalize(actual_dom) != normalize(expected_dom):
        errors.append(
            f"{example_id}: dominators mismatch: "
            f"expected={normalize(expected_dom)}, actual={normalize(actual_dom)}"
        )

    actual_idom = compute_idom(entry, vertices, actual_dom)
    expected_idom = {str(key): str(value) for key, value in example["idom"].items()}
    if dict(sorted(actual_idom.items())) != dict(sorted(expected_idom.items())):
        errors.append(
            f"{example_id}: idom mismatch: "
            f"expected={dict(sorted(expected_idom.items()))}, "
            f"actual={dict(sorted(actual_idom.items()))}"
        )

    actual_frontier = compute_frontier(vertices, pred, actual_dom)
    expected_frontier = {
        str(vertex): {str(item) for item in values}
        for vertex, values in example["frontier"].items()
    }
    if normalize(actual_frontier) != normalize(expected_frontier):
        errors.append(
            f"{example_id}: dominance frontier mismatch: "
            f"expected={normalize(expected_frontier)}, "
            f"actual={normalize(actual_frontier)}"
        )

    return errors


def main() -> int:
    document = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    if document.get("schema_version") != 1:
        print("Golden validation failed: unsupported schema_version")
        return 1

    examples = document.get("examples")
    if not isinstance(examples, list) or not examples:
        print("Golden validation failed: examples must be a non-empty list")
        return 1

    ids = [str(example.get("id")) for example in examples]
    if len(ids) != len(set(ids)):
        print("Golden validation failed: duplicate example id")
        return 1

    errors: list[str] = []
    for example in examples:
        errors.extend(validate_example(example))

    if errors:
        print("Golden validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Golden validation passed: {len(examples)} semantic CFG examples.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
