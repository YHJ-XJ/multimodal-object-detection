"""Train and evaluate M3FD RGB, thermal or four-channel RGBT YOLO11n baselines.

Run prepare_m3fd.py first. Keep the three modes on the same split_manifest.csv.
Examples:
    python train_m3fd.py --mode rgb --epochs 1
    python train_m3fd.py --mode thermal --epochs 100
    python train_m3fd.py --mode rgbt --epochs 100
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT / "数据集汇总" / "M3FD_基线准备"
RUN_ROOT = PROJECT / "基线实验" / "M3FD_YOLO11n"


def train(mode: str, data_root: Path, run_root: Path, epochs: int, batch: int, device: str = "0") -> None:
    try:
        import torch
        import ultralytics
        from ultralytics import YOLO
    except ImportError as exc:
        raise SystemExit(
            "Training needs a Python environment with CUDA-capable PyTorch and recent ultralytics. "
            "The current system Python may only be suitable for data preparation."
        ) from exc

    yaml_path = data_root / mode / "data.yaml"
    manifest = data_root / "split_manifest.csv"
    if not yaml_path.is_file():
        raise FileNotFoundError(f"Dataset YAML is missing: {yaml_path}")
    if not manifest.is_file():
        raise FileNotFoundError(f"Shared split manifest is missing: {manifest}")
    split_hash = hashlib.sha256(manifest.read_bytes()).hexdigest()
    if device != "cpu" and not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU is not available in this Python environment")
    if mode == "rgbt":
        from packaging.version import Version

        if Version(ultralytics.__version__) < Version("8.3.112"):
            raise RuntimeError("Four-channel TIFF training requires ultralytics >= 8.3.112")

    expected_channels = 4 if mode == "rgbt" else 3
    model = YOLO("yolo11n.pt")

    def verify_first_conv(trainer) -> None:
        first_conv = next(
            layer for layer in trainer.model.modules() if isinstance(layer, torch.nn.Conv2d)
        )
        if first_conv.in_channels != expected_channels:
            raise RuntimeError(
                f"{mode}: first convolution expects {first_conv.in_channels} channels, "
                f"but the dataset needs {expected_channels}. Check ultralytics version and data.yaml."
            )
        print(f"Verified model input: {first_conv.in_channels} channels")

    model.add_callback("on_train_start", verify_first_conv)
    model.train(
        data=str(yaml_path),
        project=str(run_root),
        name=mode,
        exist_ok=False,
        imgsz=640,
        epochs=epochs,
        batch=batch,
        device=device,
        seed=42,
        deterministic=True,
        workers=2,  # Stable starting point on Windows.
        cache=False,
        amp=device != "cpu",
        mosaic=0.0,
        mixup=0.0,
        hsv_h=0.0,
        hsv_s=0.0,
        hsv_v=0.0,
        fliplr=0.5,
        degrees=0.0,
        translate=0.0,
        scale=0.0,
        shear=0.0,
        perspective=0.0,
        plots=True,
    )

    best = Path(model.trainer.save_dir) / "weights" / "best.pt"
    if not best.is_file():
        raise FileNotFoundError(f"Training finished without best.pt: {best}")
    detector = YOLO(str(best))
    metrics = detector.val(
        data=str(yaml_path), split="test", imgsz=640, batch=batch, device=device,
        project=str(run_root), name=f"{mode}_test", exist_ok=False,
    )
    print(f"{mode}: mAP50={metrics.box.map50:.4f}, mAP50-95={metrics.box.map:.4f}")
    per_class = {str(detector.names[i]): float(ap) for i, ap in enumerate(metrics.box.maps)}
    for class_name, ap in per_class.items():
        print(f"  {class_name}: AP50-95={ap:.4f}")
    summary = {
        "mode": mode,
        "ultralytics_version": ultralytics.__version__,
        "split_manifest_sha256": split_hash,
        "epochs": epochs,
        "batch": batch,
        "imgsz": 640,
        "seed": 42,
        "device": device,
        "map50": float(metrics.box.map50),
        "map50_95": float(metrics.box.map),
        "per_class_map50_95": per_class,
        "weights": str(best),
    }
    (best.parent.parent / "baseline_result.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Best weights: {best}")


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
