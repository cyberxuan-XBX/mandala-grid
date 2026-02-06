#!/usr/bin/env python3
"""Tests for mandala_grid.py"""

import json
import sys
import tempfile
from pathlib import Path

from mandala_grid import MandalaGrid, GridPosition, compare_grids, mirror_analysis


def test_default_grid_has_9_positions():
    grid = MandalaGrid.default()
    assert len(grid.positions) == 9, f"Expected 9 positions, got {len(grid.positions)}"


def test_center_is_alayavijnana():
    grid = MandalaGrid.default()
    center = grid.get(0)
    assert center.consciousness == "ālayavijñāna"
    assert center.bias == 1.0


def test_position_7_highest_non_center():
    grid = MandalaGrid.default()
    top = grid.top_n(1)
    assert top[0].index == 7, f"Expected position 7 (Deconstructor), got {top[0].index}"
    assert top[0].bias == 0.95


def test_all_biases_in_range():
    grid = MandalaGrid.default()
    for p in grid.positions:
        assert 0.0 <= p.bias <= 1.0, f"Position {p.index} bias {p.bias} out of range"


def test_personality_signature():
    grid = MandalaGrid.default()
    sig = grid.personality_signature()
    assert "quan-default" in sig
    assert "Deconstructor" in sig


def test_json_roundtrip():
    grid = MandalaGrid.default()
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        f.write(grid.to_json())
        path = f.name

    loaded = MandalaGrid.from_json(path)
    assert len(loaded.positions) == 9
    assert loaded.get(7).bias == 0.95
    assert loaded.name == "quan-default"
    Path(path).unlink()


def test_weighted_prompt_contains_task():
    grid = MandalaGrid.default()
    prompt = grid.weighted_prompt("test task")
    assert "test task" in prompt
    assert "mandala grid" in prompt.lower()


def test_compare_identical_grids():
    a = MandalaGrid.default()
    b = MandalaGrid.default()
    result = compare_grids(a, b)
    # Identical grids should show no position diffs
    assert "↑" not in result and "↓" not in result


def test_compare_different_grids():
    a = MandalaGrid.default()
    b = MandalaGrid.default()
    b.positions[7].bias = 0.5  # Change position 7
    b.name = "modified"
    result = compare_grids(a, b)
    assert "↓" in result or "↑" in result


def test_mirror_analysis():
    grid = MandalaGrid.default()
    result = mirror_analysis(grid)
    assert "Mirror" in result
    assert "self-portrait" in result


def test_display_grid():
    grid = MandalaGrid.default()
    display = grid.display()
    assert "+" in display  # Has grid borders
    lines = display.strip().split("\n")
    assert len(lines) == 7  # 4 separators + 3 rows


def test_eight_consciousnesses_mapped():
    """Every position should have a consciousness mapping."""
    grid = MandalaGrid.default()
    for p in grid.positions:
        assert p.consciousness, f"Position {p.index} missing consciousness"
        assert p.consciousness_zh, f"Position {p.index} missing consciousness_zh"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {t.__name__}: {e}")
            failed += 1

    print(f"\n{'═' * 40}")
    print(f"  {passed} passed, {failed} failed, {passed + failed} total")
    print(f"{'═' * 40}")
    sys.exit(1 if failed else 0)

