"""Train LLVIP visible, infrared, or four-channel RGB-T YOLO11n baselines.

This reuses the checked training/evaluation routine from train_m3fd.py so the
three modalities share the same model and settings. Keep the official test
split untouched and compare all three modes on the same split_manifest.csv.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from train_m3fd import train


PROJECT = Path(__file__).resolve().parents[1]
DATA_ROOT = Path("D:/rgbt_data/LLVIP_prepared")
RUN_ROOT = Path("D:/rgbt_runs/LLVIP_YOLO11n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("rgb", "thermal", "rgbt"), required=True)
    parser.add_argument("--data-root", type=Path, default=DATA_ROOT)
    parser.add_argument("--run-root", type=Path, default=RUN_ROOT)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch", type=int, default=4)
    parser.add_argument("--device", default="0", help="CUDA device index; use cpu only for a small pipeline smoke test")
    args = parser.parse_args()
    train(args.mode, args.data_root, args.run_root, args.epochs, args.batch, args.device)
