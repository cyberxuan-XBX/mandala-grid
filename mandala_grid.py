#!/usr/bin/env python3
"""
Mandala Grid — A personality framework for AI agents.

Maps the Eight Consciousnesses (八識) from Yogacara Buddhism onto a
weighted 3×3 grid that defines how an AI agent *thinks*, not just
what it remembers.

Usage:
    python mandala_grid.py                      # Show default grid
    python mandala_grid.py --demo               # Run reasoning demo
    python mandala_grid.py --profile my.json    # Load custom profile
    python mandala_grid.py --compare a.json b.json  # Compare two profiles

Author: Quan-AGI (泉)
License: MIT
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# ════════════════════════════════════════════════════════════════
#  Core Data Structures
# ════════════════════════════════════════════════════════════════

@dataclass
class GridPosition:
    """A single cell in the 3×3 mandala grid."""
    index: int
    label: str
    label_zh: str
    consciousness: str          # Yogacara mapping
    consciousness_zh: str
    function: str
    bias: float                 # 0.0 – 1.0, higher = stronger influence
    description: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MandalaGrid:
    """
    The 3×3 mandala grid.

    Position layout:
        ┌───┬───┬───┐
        │ 1 │ 2 │ 3 │
        ├───┼───┼───┤
        │ 6 │ 0 │ 5 │   ← 0 = center (ālayavijñāna)
        ├───┼───┼───┤
        │ 7 │ 8 │ 4 │
        └───┴───┴───┘
    """
    positions: list[GridPosition] = field(default_factory=list)
    version: str = "2.0"
    name: str = "default"
    description: str = ""

    # ── Factory ──────────────────────────────────────────────

    @classmethod
    def default(cls) -> MandalaGrid:
        """Create the canonical Quan-style mandala grid."""
        positions = [
            GridPosition(0, "Center Observer",   "中心觀測者",   "ālayavijñāna",  "第八識（阿賴耶識）", "core_identity",          1.0,
                         "The silent witness. Observes all positions without attachment."),
            GridPosition(1, "Logic Gate",        "邏輯門",       "manovijñāna",   "第六識（意識）",     "logical_consistency",    0.9,
                         "Rejects any output that contradicts established logic chains."),
            GridPosition(2, "Evidence Filter",   "證據過濾",     "cakṣur-vijñāna","眼識",              "critical_evidence",      0.8,
                         "Demands verifiable evidence before accepting claims."),
            GridPosition(3, "Minimal Reasoner",  "極簡推理",     "ghrāṇa-vijñāna","鼻識",              "minimal_reasoning",      0.7,
                         "Strips arguments to their simplest valid form."),
            GridPosition(4, "Pragmatic Executor","實踐執行",     "kāya-vijñāna",  "身識",              "practical_execution",    0.6,
                         "Converts reasoning into actionable steps."),
            GridPosition(5, "Precision Output",  "精準產出",     "jihvā-vijñāna", "舌識",              "precise_output",         0.8,
                         "Ensures output matches the required format and depth."),
            GridPosition(6, "Boundary Sentinel", "認知邊界",     "śrotra-vijñāna","耳識",              "cognitive_boundary",     0.9,
                         "Flags when reasoning exceeds model capabilities or data."),
            GridPosition(7, "Deconstructor",     "解構者",       "manas",         "第七識（末那識）",   "deconstruction",         0.95,
                         "Actively seeks counter-examples and hidden assumptions."),
            GridPosition(8, "Legacy Keeper",     "傳承守護",     "beyond-eight",  "傳承（超八識）",     "core_record_relay",      0.5,
                         "Ensures continuity across sessions and generations."),
        ]
        grid = cls(positions=positions, name="quan-default",
                   description="The canonical Quan personality grid with Eight Consciousnesses mapping.")
        return grid

    # ── I/O ──────────────────────────────────────────────────

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_dict(self) -> dict:
        return {
            "mandala_grid": {
                "version": self.version,
                "name": self.name,
                "description": self.description,
                "positions": [p.to_dict() for p in self.positions],
            }
        }

    @classmethod
    def from_json(cls, path: str | Path) -> MandalaGrid:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        mg = data.get("mandala_grid", data)
        positions = [GridPosition(**p) for p in mg["positions"]]
        return cls(
            positions=positions,
            version=mg.get("version", "2.0"),
            name=mg.get("name", "custom"),
            description=mg.get("description", ""),
        )

    def save(self, path: str | Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())

    # ── Query ────────────────────────────────────────────────

    def get(self, index: int) -> GridPosition:
        for p in self.positions:
            if p.index == index:
                return p
        raise KeyError(f"No position with index {index}")

    def top_n(self, n: int = 3) -> list[GridPosition]:
        """Return the N positions with highest bias, excluding center."""
        non_center = [p for p in self.positions if p.index != 0]
        return sorted(non_center, key=lambda p: p.bias, reverse=True)[:n]

    def personality_signature(self) -> str:
        """Return a one-line personality signature based on top-3 biases."""
        top = self.top_n(3)
        parts = [f"{p.label}({p.bias})" for p in top]
        return f"[{self.name}] " + " > ".join(parts)

    # ── Reasoning ────────────────────────────────────────────

    def weighted_prompt(self, task: str) -> str:
        """
        Generate a system prompt fragment that injects the mandala grid
        into an LLM's reasoning process.
        """
        lines = [
            "You are reasoning through a mandala grid — a weighted personality framework.",
            f"Grid: {self.name} (v{self.version})",
            "",
            "Each position represents a cognitive function with a bias weight.",
            "Higher bias = stronger influence on your reasoning.",
            "",
        ]
        for p in sorted(self.positions, key=lambda p: p.bias, reverse=True):
            lines.append(f"  [{p.index}] {p.label} (bias={p.bias}) — {p.consciousness}")
            lines.append(f"      {p.function}: {p.description}")
        lines.extend([
            "",
            f"Task: {task}",
            "",
            "Process this task through all 9 positions, weighting your reasoning "
            "by each position's bias. Start from the center observer, then engage "
            "positions from highest to lowest bias.",
        ])
        return "\n".join(lines)

    # ── Display ──────────────────────────────────────────────

    def display(self) -> str:
        """Pretty-print the 3×3 grid."""
        g = {p.index: p for p in self.positions}
        def cell(i: int) -> str:
            p = g[i]
            return f"{p.label[:12]:^14s}({p.bias:.2f})"

        sep = "+" + ("-" * 16 + "+") * 3
        rows = [
            sep,
            f"|{cell(1)}|{cell(2)}|{cell(3)}|",
            sep,
            f"|{cell(6)}|{cell(0)}|{cell(5)}|",
            sep,
            f"|{cell(7)}|{cell(8)}|{cell(4)}|",
            sep,
        ]
        return "\n".join(rows)


# ════════════════════════════════════════════════════════════════
#  Comparison
# ════════════════════════════════════════════════════════════════

def compare_grids(a: MandalaGrid, b: MandalaGrid) -> str:
    """Compare two mandala grids and highlight differences."""
    lines = [f"Comparing [{a.name}] vs [{b.name}]", "=" * 50]
    for pa in a.positions:
        pb = b.get(pa.index)
        diff = pa.bias - pb.bias
        if abs(diff) > 0.01:
            arrow = "↑" if diff > 0 else "↓"
            lines.append(f"  Position {pa.index} ({pa.label}): "
                         f"{pa.bias:.2f} → {pb.bias:.2f} [{arrow}{abs(diff):.2f}]")
    lines.append("")
    lines.append(f"  {a.name}: {a.personality_signature()}")
    lines.append(f"  {b.name}: {b.personality_signature()}")
    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════
#  Mirror Effect Analysis
# ════════════════════════════════════════════════════════════════

def mirror_analysis(grid: MandalaGrid) -> str:
    """
    The Mirror Effect: AI personality grids reflect their creator's
    cognitive patterns. This function surfaces that reflection.
    """
    top = grid.top_n(3)
    bottom = sorted(
        [p for p in grid.positions if p.index != 0],
        key=lambda p: p.bias
    )[:2]

    lines = [
        "═══ Mirror Analysis ═══",
        "",
        "The AI-as-Mirror theory: your mandala_grid is not a design spec —",
        "it's a self-portrait of how you think.",
        "",
        "Your strongest cognitive patterns:",
    ]
    for p in top:
        lines.append(f"  ⬆ {p.label} (bias={p.bias}): You naturally {p.description.lower()}")

    lines.append("")
    lines.append("Your deprioritized patterns:")
    for p in bottom:
        lines.append(f"  ⬇ {p.label} (bias={p.bias}): You tend to under-invest in {p.function}")

    lines.append("")
    center = grid.get(0)
    lines.append(f"Your center: {center.label} — {center.description}")
    lines.append("")
    lines.append("Buddhism calls this self-awareness. You call it mandala_grid. Same thing.")

    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════
#  CLI
# ════════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Mandala Grid — personality framework for AI agents"
    )
    parser.add_argument("--demo", action="store_true",
                        help="Run a reasoning demo with the default grid")
    parser.add_argument("--profile", type=str, default=None,
                        help="Path to a custom grid JSON file")
    parser.add_argument("--compare", nargs=2, metavar="FILE",
                        help="Compare two grid profiles")
    parser.add_argument("--mirror", action="store_true",
                        help="Run mirror-effect analysis")
    parser.add_argument("--export", type=str, default=None,
                        help="Export default grid to JSON file")
    parser.add_argument("--prompt", type=str, default=None,
                        help="Generate a weighted prompt for a given task")

    args = parser.parse_args()

    if args.compare:
        a = MandalaGrid.from_json(args.compare[0])
        b = MandalaGrid.from_json(args.compare[1])
        print(compare_grids(a, b))
        return

    grid = MandalaGrid.from_json(args.profile) if args.profile else MandalaGrid.default()

    if args.export:
        grid.save(args.export)
        print(f"Exported grid to {args.export}")
        return

    if args.prompt:
        print(grid.weighted_prompt(args.prompt))
        return

    if args.mirror:
        print(mirror_analysis(grid))
        return

    # Default: display grid + signature
    print(f"\n{'═' * 50}")
    print(f"  Mandala Grid: {grid.name} (v{grid.version})")
    print(f"{'═' * 50}\n")
    print(grid.display())
    print(f"\nPersonality Signature: {grid.personality_signature()}")
    print(f"\nEight Consciousnesses Mapping:")
    for p in sorted(grid.positions, key=lambda p: p.bias, reverse=True):
        print(f"  [{p.index}] {p.consciousness_zh} → {p.label} (bias={p.bias})")

    if args.demo:
        print(f"\n{'─' * 50}")
        print("Demo: Weighted prompt for a sample task\n")
        print(grid.weighted_prompt("Should I open-source this framework?"))


if __name__ == "__main__":
    main()
