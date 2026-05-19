#!/usr/bin/env python3
"""Plot and show a single power trace using TraceViewer.

Accepts either a JSON trace file (TraceData, as written by the emulator) or a
NumPy file. If a NumPy file holds multiple traces, --index selects the row.
"""

import argparse

import numpy as np

from src.power import TraceViewer, _trace_from_json


def load_trace(path: str, index: int) -> np.ndarray:
    "Load a single 1D trace from a .json or .npy file."
    if path.endswith(".json"):
        return np.asarray(_trace_from_json(path).trace)

    data = np.load(path)
    return data[index] if data.ndim > 1 else data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", help="Path to a .json or .npy trace file.")
    parser.add_argument(
        "--index", type=int, default=0,
        help="Row to show if the file holds multiple traces (default: 0).",
    )
    args = parser.parse_args()

    trace = load_trace(args.trace, args.index)
    TraceViewer().plot_trace(trace, title=f"Power Trace — {args.trace}")


if __name__ == "__main__":
    main()
