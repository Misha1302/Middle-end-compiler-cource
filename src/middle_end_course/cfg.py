from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping


@dataclass(frozen=True, slots=True)
class ControlFlowGraph:
    """Immutable control-flow graph.

    The class owns only graph structure and structural invariants. Algorithms live in
    :mod:`middle_end_course.analysis`; convenience methods below delegate to them so
    existing course examples remain compact.
    """

    entry: str
    successors: Mapping[str, tuple[str, ...]]

    @classmethod
    def from_mapping(
        cls,
        entry: str,
        successors: Mapping[str, Iterable[str]],
    ) -> "ControlFlowGraph":
        if not isinstance(entry, str) or not entry:
            raise ValueError("entry must be a non-empty string")

        normalized: dict[str, tuple[str, ...]] = {}
        for node, targets in successors.items():
            if not isinstance(node, str) or not node:
                raise ValueError("node names must be non-empty strings")
            target_tuple = tuple(targets)
            if any(not isinstance(target, str) or not target for target in target_tuple):
                raise ValueError(f"successors of {node!r} must be non-empty strings")
            if len(set(target_tuple)) != len(target_tuple):
                raise ValueError(f"duplicate successors for node {node!r}")
            normalized[node] = target_tuple

        graph = cls(entry=entry, successors=MappingProxyType(normalized))
        graph.validate()
        return graph

    @property
    def nodes(self) -> frozenset[str]:
        return frozenset(self.successors)

    def validate(self) -> None:
        if self.entry not in self.successors:
            raise ValueError(f"entry node {self.entry!r} is not declared")

        unknown = sorted(
            {
                target
                for targets in self.successors.values()
                for target in targets
                if target not in self.successors
            }
        )
        if unknown:
            raise ValueError(f"edges reference unknown nodes: {unknown}")

    def predecessors(self) -> Mapping[str, tuple[str, ...]]:
        result: dict[str, list[str]] = {node: [] for node in self.successors}
        for source, targets in self.successors.items():
            for target in targets:
                result[target].append(source)
        return MappingProxyType(
            {node: tuple(sorted(preds)) for node, preds in result.items()}
        )

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

    # Compatibility-oriented convenience façade. Core algorithms remain separate.
    def dominators(self) -> Mapping[str, frozenset[str]]:
        from .analysis import analyze_dominators

        return analyze_dominators(self).dominators

    def immediate_dominators(self) -> Mapping[str, str | None]:
        from .analysis import compute_immediate_dominators

        return compute_immediate_dominators(self)

    def dominance_frontier(self) -> Mapping[str, frozenset[str]]:
        from .analysis import compute_dominance_frontier

        return compute_dominance_frontier(self)

    def natural_loop(self, header: str, latch: str) -> frozenset[str]:
        from .analysis import analyze_natural_loop

        return analyze_natural_loop(self, header=header, latch=latch).nodes
