"""Audit LLVIP VOC annotations before converting them to YOLO labels."""

from __future__ import annotations

import json
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

from prepare_llvip import DEFAULT_ARCHIVE, index_archive


def audit(archive: Path) -> dict:
    classes = Counter()
    issues = Counter()
    examples: dict[str, list] = {}
    objects = 0
    with zipfile.ZipFile(archive) as zf:
        entries = index_archive(zf)["annotations"]["all"]
        for stem, member in entries.items():
            root = ET.fromstring(zf.read(member))
            size = root.find("size")
            width = int(size.findtext("width"))
            height = int(size.findtext("height"))
            for obj in root.findall("object"):
                objects += 1
                name = (obj.findtext("name") or "").lower().strip()
                classes[name] += 1
                box = obj.find("bndbox")
                coords = tuple(float(box.findtext(tag, "nan")) for tag in ("xmin", "ymin", "xmax", "ymax"))
                x1, y1, x2, y2 = coords
                reason = None
                if name != "person":
                    reason = "unexpected_class"
                elif not (x1 < x2 and y1 < y2):
                    reason = "degenerate"
                elif not (0 <= x1 and 0 <= y1 and x2 <= width and y2 <= height):
                    reason = "out_of_bounds"
                if reason:
                    issues[reason] += 1
                    examples.setdefault(reason, []).append({"id": stem, "box": coords, "image_size": (width, height)})
    return {
        "annotations": len(entries),
        "objects": objects,
        "classes": dict(classes),
        "issues": dict(issues),
        "issue_examples": {key: value[:25] for key, value in examples.items()},
    }


if __name__ == "__main__":
    print(json.dumps(audit(DEFAULT_ARCHIVE), ensure_ascii=False, indent=2))
