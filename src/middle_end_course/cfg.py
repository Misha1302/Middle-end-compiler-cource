from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class ControlFlowGraph:
    """A small immutable CFG intended for manual experiments and tests."""

    entry: str
    successors: Mapping[str, tuple[str, ...]]

    @classmethod
    def from_mapping(
        cls,
        entry: str,
        successors: Mapping[str, Iterable[str]],
    ) -> "ControlFlowGraph":
        normalized = {node: tuple(targets) for node, targets in successors.items()}
        graph = cls(entry=entry, successors=normalized)
        graph.validate()
        return graph

    @property
    def nodes(self) -> frozenset[str]:
        return frozenset(self.successors)

    def validate(self) -> None:
        if self.entry not in self.successors:
            raise ValueError(f"entry node {self.entry!r} is not declared")
        unknown = {
            target
            for targets in self.successors.values()
            for target in targets
            if target not in self.successors
        }
        if unknown:
            raise ValueError(f"edges reference unknown nodes: {sorted(unknown)}")

    def predecessors(self) -> dict[str, tuple[str, ...]]:
        result: dict[str, list[str]] = {node: [] for node in self.successors}
        for source, targets in self.successors.items():
            for target in targets:
                result[target].append(source)
        return {node: tuple(preds) for node, preds in result.items()}

    def reachable(self) -> frozenset[str]:
        visited: set[str] = set()
        stack = [self.entry]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            stack.extend(reversed(self.successors[node]))
        return frozenset(visited)

    def dominators(self) -> dict[str, frozenset[str]]:
        reachable = self.reachable()
        preds = self.predecessors()
        dom: dict[str, set[str]] = {
            node: ({node} if node == self.entry else set(reachable))
            for node in reachable
        }

        changed = True
        while changed:
            changed = False
            for node in sorted(reachable):
                if node == self.entry:
                    continue
                reachable_preds = [pred for pred in preds[node] if pred in reachable]
                if not reachable_preds:
                    new_value = {node}
                else:
                    intersection = set(dom[reachable_preds[0]])
                    for pred in reachable_preds[1:]:
                        intersection.intersection_update(dom[pred])
                    new_value = {node} | intersection
                if new_value != dom[node]:
                    dom[node] = new_value
                    changed = True
        return {node: frozenset(value) for node, value in dom.items()}

    def immediate_dominators(self) -> dict[str, str | None]:
        dom = self.dominators()
        result: dict[str, str | None] = {self.entry: None}
        for node in sorted(dom):
            if node == self.entry:
                continue
            strict = set(dom[node]) - {node}
            candidates = [
                candidate
                for candidate in strict
                if (strict - {candidate}).issubset(dom[candidate])
            ]
            if len(candidates) != 1:
                raise RuntimeError(
                    f"expected one immediate dominator for {node!r}, got {candidates}"
                )
            result[node] = candidates[0]
        return result

    def dominance_frontier(self) -> dict[str, frozenset[str]]:
        """Compute DF from its definition; intentionally simple, not optimized."""
        dom = self.dominators()
        preds = self.predecessors()
        reachable = set(dom)
        frontier: dict[str, set[str]] = {node: set() for node in reachable}

        for x in reachable:
            for y in reachable:
                x_strictly_dominates_y = x in (set(dom[y]) - {y})
                if x_strictly_dominates_y:
                    continue
                if any(pred in reachable and x in dom[pred] for pred in preds[y]):
                    frontier[x].add(y)
        return {node: frozenset(values) for node, values in frontier.items()}

    def natural_loop(self, header: str, latch: str) -> frozenset[str]:
        if header not in self.nodes or latch not in self.nodes:
            raise ValueError("header and latch must be declared nodes")
        if header not in self.successors[latch]:
            raise ValueError(f"{latch!r} -> {header!r} is not an edge")
        dom = self.dominators()
        if header not in dom.get(latch, frozenset()):
            raise ValueError("the edge is not a back edge: header does not dominate latch")

        preds = self.predecessors()
        loop = {header, latch}
        worklist = [latch]
        while worklist:
            node = worklist.pop()
            for pred in preds[node]:
                if pred not in loop:
                    loop.add(pred)
                    if pred != header:
                        worklist.append(pred)
        return frozenset(loop)
