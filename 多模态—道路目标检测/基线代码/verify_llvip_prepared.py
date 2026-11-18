"""Verify LLVIP paired splits, labels, and four-channel TIFFs after conversion."""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter
from pathlib import Path

import cv2
import numpy as np


def verify(root: Path, sample_count: int = 12) -> dict:
    root = root.resolve()
    summary = json.loads((root / "preparation_summary.json").read_text(encoding="utf-8"))
    with (root / "split_manifest.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)) or len(ids) != sum(summary["pairs"].values()):
        raise AssertionError("Manifest contains duplicate or missing IDs")
    counts = Counter(row["split"] for row in rows)
    if dict(counts) != summary["pairs"]:
        raise AssertionError("Manifest split counts differ from summary")
    if any((row["source_split"] == "test") != (row["split"] == "test") for row in rows):
        raise AssertionError("Author test set leaked into train/validation")
    train_groups = {row["prefix_group"] for row in rows if row["split"] == "train"}
    val_groups = {row["prefix_group"] for row in rows if row["split"] == "val"}
    if train_groups & val_groups:
        raise AssertionError("Train and validation filename-prefix groups overlap")

    by_split = {split: {row["id"] for row in rows if row["split"] == split} for split in ("train", "val", "test")}
    for mode in summary["modes"]:
        for split, expected in by_split.items():
            images = {path.stem for path in (root / mode / "images" / split).iterdir() if path.is_file()}
            labels = {path.stem for path in (root / mode / "labels" / split).glob("*.txt")}
            if images != expected or labels != expected:
                raise AssertionError(f"{mode}/{split}: image or label IDs differ from manifest")

    checked_boxes = Counter()
    for row in rows:
        stem, split = row["id"], row["split"]
        label_files = [(root / mode / "labels" / split / f"{stem}.txt") for mode in summary["modes"]]
        raw = label_files[0].read_bytes()
        if any(path.read_bytes() != raw for path in label_files[1:]):
            raise AssertionError(f"{stem}: labels differ across modalities")
        lines = raw.decode("utf-8").splitlines()
        if len(lines) != int(row["boxes"]):
            raise AssertionError(f"{stem}: box count differs from manifest")
        for line in lines:
            fields = line.split()
            if len(fields) != 5 or fields[0] != "0" or any(not 0 <= float(value) <= 1 for value in fields[1:]):
                raise AssertionError(f"{stem}: invalid YOLO label {line!r}")
        checked_boxes[split] += len(lines)
    if dict(checked_boxes) != summary["boxes"]:
        raise AssertionError("Box totals differ from summary")

    samples = random.Random(42).sample(rows, min(sample_count, len(rows)))
    for row in samples:
        stem, split = row["id"], row["split"]
        rgb_path = next((root / "rgb" / "images" / split).glob(f"{stem}.*"))
        t_path = next((root / "thermal" / "images" / split).glob(f"{stem}.*"))
        rgb = cv2.imread(str(rgb_path), cv2.IMREAD_COLOR)
        thermal = cv2.imread(str(t_path), cv2.IMREAD_GRAYSCALE)
        ok, planes = cv2.imreadmulti(str(root / "rgbt" / "images" / split / f"{stem}.tiff"), flags=cv2.IMREAD_UNCHANGED)
        if rgb is None or thermal is None or not ok or len(planes) != 4:
            raise AssertionError(f"{stem}: unreadable paired image or TIFF")
        b, g, r = cv2.split(rgb)
        if not all(np.array_equal(a, b_) for a, b_ in zip((r, g, b, thermal), planes)):
            raise AssertionError(f"{stem}: TIFF channels do not match paired images")

    report = {"status": "passed", "pairs": dict(counts), "boxes": dict(checked_boxes), "checked_tiff_pairs": len(samples), "train_val_group_overlap": 0}
    (root / "verification_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("D:/rgbt_data/LLVIP_prepared"))
    parser.add_argument("--sample-count", type=int, default=12)
    args = parser.parse_args()
    print(json.dumps(verify(args.root, args.sample_count), indent=2))
