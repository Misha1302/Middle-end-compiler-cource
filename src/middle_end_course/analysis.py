from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .cfg import ControlFlowGraph


FrozenSetsByNode = Mapping[str, frozenset[str]]


def _freeze_sets(values: Mapping[str, set[str] | frozenset[str]]) -> FrozenSetsByNode:
    return MappingProxyType(
        {node: frozenset(items) for node, items in sorted(values.items())}
    )


@dataclass(frozen=True, slots=True)
class DominatorIteration:
    index: int
    dominators: FrozenSetsByNode
    changed_nodes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DominatorAnalysis:
    dominators: FrozenSetsByNode
    iterations: tuple[DominatorIteration, ...]


@dataclass(frozen=True, slots=True)
class NaturalLoopStep:
    popped: str
    considered_predecessors: tuple[str, ...]
    added_nodes: tuple[str, ...]
    loop_after_step: frozenset[str]


@dataclass(frozen=True, slots=True)
class NaturalLoopAnalysis:
    header: str
    latch: str
    nodes: frozenset[str]
    steps: tuple[NaturalLoopStep, ...]


def analyze_dominators(graph: ControlFlowGraph) -> DominatorAnalysis:
    """Compute dominators and retain every pedagogically relevant iteration."""

    reachable = graph.reachable()
    predecessors = graph.predecessors()
    dominators: dict[str, set[str]] = {
        node: ({node} if node == graph.entry else set(reachable))
        for node in sorted(reachable)
    }

    iterations: list[DominatorIteration] = [
        DominatorIteration(
            index=0,
            dominators=_freeze_sets(dominators),
            changed_nodes=tuple(sorted(reachable)),
        )
    ]

    index = 1
    while True:
        changed: list[str] = []
        next_values = {node: set(value) for node, value in dominators.items()}

        for node in sorted(reachable):
            if node == graph.entry:
                continue
            reachable_preds = [
                pred for pred in predecessors[node] if pred in reachable
            ]
            if not reachable_preds:
                new_value = {node}
            else:
                intersection = set(dominators[reachable_preds[0]])
                for pred in reachable_preds[1:]:
                    intersection.intersection_update(dominators[pred])
                new_value = {node} | intersection

            if new_value != dominators[node]:
                next_values[node] = new_value
                changed.append(node)

        dominators = next_values
        iterations.append(
            DominatorIteration(
                index=index,
                dominators=_freeze_sets(dominators),
                changed_nodes=tuple(changed),
            )
        )
        if not changed:
            break
        index += 1

    return DominatorAnalysis(
        dominators=_freeze_sets(dominators),
        iterations=tuple(iterations),
    )


def compute_immediate_dominators(
    graph: ControlFlowGraph,
    dominators: FrozenSetsByNode | None = None,
) -> Mapping[str, str | None]:
    dom = dominators or analyze_dominators(graph).dominators
    result: dict[str, str | None] = {graph.entry: None}

    for node in sorted(dom):
        if node == graph.entry:
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

    return MappingProxyType(result)


def compute_dominance_frontier(
    graph: ControlFlowGraph,
    dominators: FrozenSetsByNode | None = None,
) -> FrozenSetsByNode:
    """Definition-oriented DF implementation suitable for small teaching graphs."""

    dom = dominators or analyze_dominators(graph).dominators
    predecessors = graph.predecessors()
    reachable = set(dom)
    frontier: dict[str, set[str]] = {node: set() for node in reachable}

    for x in sorted(reachable):
        for y in sorted(reachable):
            if x in (set(dom[y]) - {y}):
                continue
            if any(pred in reachable and x in dom[pred] for pred in predecessors[y]):
                frontier[x].add(y)

    return _freeze_sets(frontier)


def analyze_natural_loop(
    graph: ControlFlowGraph,
    *,
    header: str,
    latch: str,
) -> NaturalLoopAnalysis:
    if header not in graph.nodes or latch not in graph.nodes:
        raise ValueError("header and latch must be declared nodes")

    reachable = graph.reachable()
    if header not in reachable or latch not in reachable:
        raise ValueError("header and latch must be reachable from entry")
    if header not in graph.successors[latch]:
        raise ValueError(f"{latch!r} -> {header!r} is not an edge")

    dominators = analyze_dominators(graph).dominators
    if header not in dominators[latch]:
        raise ValueError("the edge is not a back edge: header does not dominate latch")

    predecessors = graph.predecessors()
    loop = {header, latch}
    worklist = [] if header == latch else [latch]
    steps: list[NaturalLoopStep] = []

    while worklist:
        node = worklist.pop()
        considered = tuple(predecessors[node])
        added: list[str] = []
        for pred in considered:
            if pred not in reachable or pred in loop:
                continue
            loop.add(pred)
            added.append(pred)
            if pred != header:
                worklist.append(pred)
        steps.append(
            NaturalLoopStep(
                popped=node,
                considered_predecessors=considered,
                added_nodes=tuple(added),
                loop_after_step=frozenset(loop),
            )
        )

    return NaturalLoopAnalysis(
        header=header,
        latch=latch,
        nodes=frozenset(loop),
        steps=tuple(steps),
    )
