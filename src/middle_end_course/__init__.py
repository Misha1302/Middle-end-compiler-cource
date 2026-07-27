"""Teaching utilities for the Middle-end Compiler Course."""

from .analysis import (
    DominatorAnalysis,
    DominatorIteration,
    NaturalLoopAnalysis,
    NaturalLoopStep,
    analyze_dominators,
    analyze_natural_loop,
    compute_dominance_frontier,
    compute_immediate_dominators,
)
from .cfg import ControlFlowGraph

__all__ = [
    "ControlFlowGraph",
    "DominatorAnalysis",
    "DominatorIteration",
    "NaturalLoopAnalysis",
    "NaturalLoopStep",
    "analyze_dominators",
    "analyze_natural_loop",
    "compute_dominance_frontier",
    "compute_immediate_dominators",
]
