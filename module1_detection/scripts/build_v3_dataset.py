import shutil
import yaml
import json
import random
from pathlib import Path
from collections import Counter

random.seed(42)

# ══════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════
V3_RAW   = Path(r"C:\SWOS\module1_detection\data\v3_raw")
OUTPUT   = Path(r"C:\SWOS\module1_detection\data\waste_dataset_v3")
CLASSES  = ["plastic", "organic", "metal", "glass", "hazardous"]
CLS_IDX  = {c: i for i, c in enumerate(CLASSES)}

# Create output folders
for split in ["train", "val", "test"]:
    (OUTPUT / "images" / split).mkdir(parents=True, exist_ok=True)
    (OUTPUT / "labels" / split).mkdir(parents=True, exist_ok=True)

# ══════════════════════════════════════════════════════
# ALL DATASETS — paths and class mappings
# ══════════════════════════════════════════════════════
DATASETS = [

    # ── PLASTIC ──────────────────────────────────────
    {
        "name"   : "plastic1",
        "base"   : V3_RAW / "plastic/dataset1/Plastic waste 2.yolov8",
        "mapping": {
            0: "plastic",  # Non stretch bag
            1: None,       # OTHERS — skip
            2: "plastic",  # PET bottle
            3: "plastic",  # PET color bottle
            4: "plastic",  # PET-PS packaging
            5: "plastic",  # PP-PE bottle
            6: "plastic",  # PP-PS packaging
            7: "plastic",  # stretch bag
        },
    },
    {
        "name"   : "plastic2",
        "base"   : V3_RAW / "plastic/dataset2/Plastic Waste Management.v1i.yolov8",
        "mapping": {
            0: "plastic",  # plastic bag
            1: "plastic",  # plastic bottle
            2: "plastic",  # plastic container
            3: "plastic",  # plastic cup
            4: "plastic",  # plastic straw
            5: "plastic",  # plastic utensil
        },
    },

    # ── ORGANIC ───────────────────────────────────────
    {
        "name"   : "organic",
        "base"   : V3_RAW / "organic/Organic Waste.v1i.yolov8",
        "mapping": {
            0: "organic",  # Organic Waste
            1: "organic",  # Paper Waste
        },
    },

    # ── METAL ─────────────────────────────────────────
    {
        "name"   : "metal",
        "base"   : V3_RAW / "metal",
        "mapping": {0: "metal"},
    },

    # ── GLASS ─────────────────────────────────────────
    {
        "name"   : "glass",
        "base"   : V3_RAW / "glass",
        "mapping": {0: "glass"},
    },

    # ── HAZARDOUS ─────────────────────────────────────
    {
        "name"   : "hazardous_capy",
        "base"   : V3_RAW / "roboflow_hazardous/capy",
        "mapping": {0: "hazardous"},
    },
    {
        "name"   : "hazardous_mysterious",
        "base"   : V3_RAW / "roboflow_hazardous/mysterious",
        "mapping": {0: "hazardous"},
    },

    # ── GARBAGE CLASSIFICATION ────────────────────────
    # Has plastic, glass, metal, organic all in one
    {
        "name"   : "garbage_clf",
        "base"   : V3_RAW / "garbage classification/GARBAGE CLASSIFICATION 3.v1i.yolov8",
        "mapping": {
            0: "organic",  # BIODEGRADABLE
            1: "organic",  # CARDBOARD
            2: "glass",    # GLASS
            3: "metal",    # METAL
            4: "organic",  # PAPER
            5: "plastic",  # PLASTIC
        },
    },

    # ── TACO (YOLOv8 version from v3_raw) ─────────────
    {
        "name"   : "taco",
        "base"   : V3_RAW / "taco/TACO dataset.v1i.yolov8",
        "mapping": {
            0: "organic",  # cardboard
            1: "glass",    # glass
            2: "metal",    # metal
            3: None,       # other — skip
            4: "organic",  # paper
            5: "plastic",  # plastic
        },
    },
]

# ══════════════════════════════════════════════════════
# MERGE FUNCTION
# ══════════════════════════════════════════════════════
def process_dataset(name, base, mapping):
    copied  = 0
    skipped = 0

    for split, src_split in [
        ("train", "train"),
        ("val",   "valid"),
        ("test",  "test"),
    ]:
        src_img = base / src_split / "images"
        src_lbl = base / src_split / "labels"

        if not src_img.exists() or not src_lbl.exists():
            # try without subfolder
            src_img = base / "images" / split
            src_lbl = base / "labels" / split
            if not src_img.exists():
                continue

        for lf in src_lbl.glob("*.txt"):
            lines     = lf.read_text().strip().splitlines()
            new_lines = []

            for line in lines:
                if not line.strip():
                    continue
                parts    = line.split()
                cls_id   = int(parts[0])
                swos_cls = mapping.get(cls_id)

                if swos_cls is None:
                    continue

                new_lines.append(
                    f"{CLS_IDX[swos_cls]} {' '.join(parts[1:])}"
                )

            if not new_lines:
                skipped += 1
                continue

            # Find image file
            img_file = None
            for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
                c = src_img / f"{lf.stem}{ext}"
                if c.exists():
                    img_file = c
                    break

            if not img_file:
                skipped += 1
                continue

            # Save with unique prefix
            new_stem = f"{name}_{lf.stem}"
            shutil.copy2(
                img_file,
                OUTPUT / "images" / split / f"{new_stem}{img_file.suffix}"
            )
            (OUTPUT / "labels" / split / f"{new_stem}.txt").write_text(
                "\n".join(new_lines)
            )
            copied += 1

    return copied, skipped


# ══════════════════════════════════════════════════════
# RUN ALL DATASETS
# ══════════════════════════════════════════════════════
print("=" * 55)
print("BUILDING V3 DATASET")
print("=" * 55)

total_copied  = 0
total_skipped = 0

for ds in DATASETS:
    if not ds["base"].exists():
        print(f"\n⚠️  SKIPPED (folder not found): {ds['name']}")
        print(f"   Path: {ds['base']}")
        continue

    copied, skipped = process_dataset(
        ds["name"], ds["base"], ds["mapping"]
    )
    total_copied  += copied
    total_skipped += skipped
    print(f"\n✅ {ds['name']:<25} copied={copied:<6} skipped={skipped}")

# ══════════════════════════════════════════════════════
# WRITE data.yaml
# ══════════════════════════════════════════════════════
yaml_text = f"""path: {OUTPUT}
train: images/train
val:   images/val
test:  images/test

nc: 5
names:
  0: plastic
  1: organic
  2: metal
  3: glass
  4: hazardous
"""
(OUTPUT / "data.yaml").write_text(yaml_text)
print(f"\n✅ data.yaml written")

# ══════════════════════════════════════════════════════
# FINAL STATS
# ══════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("CLASS DISTRIBUTION (train annotations)")
print("=" * 55)

counts = Counter()
for lf in (OUTPUT / "labels" / "train").glob("*.txt"):
    for line in lf.read_text().strip().splitlines():
        if line.strip():
            counts[int(line.split()[0])] += 1

for idx, name in enumerate(CLASSES):
    bar  = "█" * min(counts[idx] // 100, 40)
    flag = " ⚠️  NEEDS MORE" if counts[idx] < 500 else " ✅"
    print(f"  {idx} {name:<12} {counts[idx]:>7} annotations  {flag}")
    print(f"    {bar}")

print("\n" + "=" * 55)
print("IMAGE COUNTS PER SPLIT")
print("=" * 55)
for split in ["train", "val", "test"]:
    n = len(list((OUTPUT / "images" / split).glob("*.*")))
    print(f"  {split:<8} {n:>6} images")

print(f"\n  Total copied : {total_copied}")
print(f"  Total skipped: {total_skipped}")
print(f"\n  Output: {OUTPUT}")
print(f"  Ready to zip and upload to Colab!")