"""Apply the current deterministic LLVIP validation split to prepared files."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from prepare_llvip import split_train


def repartition(root: Path) -> dict:
    root = root.resolve()
    summary_path = root / "preparation_summary.json"
    manifest_path = root / "split_manifest.csv"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    with manifest_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fields = reader.fieldnames
        rows = list(reader)
    source_train = [row["id"] for row in rows if row["source_split"] == "train"]
    desired = split_train(source_train, summary["seed"], summary["val_fraction"])
    changes = [row for row in rows if row["source_split"] == "train" and row["split"] != desired[row["id"]]]

    # Check every path before moving any file. A rerun can finish after an interruption.
    moves: list[tuple[Path, Path]] = []
    for row in changes:
        stem, target_split = row["id"], desired[row["id"]]
        for mode in summary["modes"]:
            for kind in ("images", "labels"):
                target_dir = root / mode / kind / target_split
                source_dir = root / mode / kind / row["split"]
                if kind == "images":
                    suffixes = (".tiff",) if mode == "rgbt" else (".jpg", ".jpeg", ".png")
                    candidates = [path for directory in (source_dir, target_dir) for suffix in suffixes
                                  if (path := directory / f"{stem}{suffix}").exists()]
                else:
                    candidates = [path for path in (source_dir / f"{stem}.txt", target_dir / f"{stem}.txt") if path.exists()]
                if len(candidates) != 1:
                    raise RuntimeError(f"{stem}: expected one {mode}/{kind} file across old and new splits")
                src = candidates[0]
                dst = target_dir / src.name
                if not src.resolve().is_relative_to(root) or not dst.resolve().is_relative_to(root):
                    raise RuntimeError(f"Refusing path outside prepared dataset: {src} -> {dst}")
                if src != dst:
                    if dst.exists():
                        raise FileExistsError(dst)
                    moves.append((src, dst))
    for src, dst in moves:
        src.replace(dst)

    for row in changes:
        row["split"] = desired[row["id"]]
    temp_manifest = manifest_path.with_suffix(".csv.tmp")
    with temp_manifest.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temp_manifest.replace(manifest_path)
    summary["pairs"] = dict(Counter(row["split"] for row in rows))
    summary["boxes"] = dict(Counter({split: sum(int(row["boxes"]) for row in rows if row["split"] == split) for split in ("train", "val", "test")}))
    summary["actual_val_fraction_of_author_train"] = summary["pairs"]["val"] / len(source_train)
    summary["split_method"] = "seeded whole two-digit filename-prefix groups; stop before large overshoot"
    temp_summary = summary_path.with_suffix(".json.tmp")
    temp_summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    temp_summary.replace(summary_path)
    return {"changed_pairs": len(changes), "moved_files": len(moves), "pairs": summary["pairs"], "boxes": summary["boxes"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("D:/rgbt_data/LLVIP_prepared"))
    args = parser.parse_args()
    print(json.dumps(repartition(args.root), indent=2))
