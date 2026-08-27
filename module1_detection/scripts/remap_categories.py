import json
import os
import shutil
import random
from pathlib import Path

# ── Paths ──────────────────────────────────────────────
TACO_JSON  = Path(r"C:\SWOS\module1_detection\data\TACO\data\annotations.json")
IMAGES_DIR = Path(r"C:\SWOS\module1_detection\data\TACO\data")
OUTPUT_DIR = Path(r"C:\SWOS\module1_detection\data\waste_dataset")

# ── Your 5 SWOS classes ────────────────────────────────
# Based on YOUR actual TACO category distribution
REMAP = {
    "plastic": [
        "Plastic film",
        "Clear plastic bottle",
        "Other plastic",
        "Other plastic wrapper",
        "Plastic bottle cap",
        "Plastic straw",
        "Plastic lid",
        "Disposable plastic cup",
        "Foam cup",
        "Other plastic cup",
        "Plastic bag & wrapper",
        "Six pack rings",
        "Plastic gloves",
        "Plastic utensils",
        "Foam food container",
        "Plastic container",
        "Single-use carrier bag",
        "Polypropylene bag",
        "Other plastic bottle",
        "Garbage bag",
        "Plastified paper bag",
        "Crisp packet",
        "Spread tub",
        "Tupperware",
        "Disposable food container",
        "Other plastic container",
        "Plastic glooves",
        "Squeezable tube",
        "Styrofoam piece",
    ],
    "organic": [
        "Cigarette",          # 667 samples — your strongest class
        "Paper",
        "Paper bag",
        "Newspaper & magazine",
        "Paper cup",
        "Meal carton",
        "Pizza box",
        "Egg carton",
        "Toilet tube",
        "Magazine paper",
        "Food waste",
        "Tissues & napkins",
        "Wrapping paper",
        "Normal paper",
        "Paper straw",
        "Tissues",
        "Other carton",
        "Drink carton",
        "Corrugated carton",
        
    ],
    "metal": [
        "Drink can",
        "Aerosol",
        "Metal bottle cap",
        "Metal lid",
        "Aluminium foil",
        "Aluminium blister pack",
        "Carded blister pack",
        "Other metal",
        "Tin",
        "Food Can",
        "Pop tab",
    ],
    "glass": [
        "Glass bottle",
        "Broken glass",
        "Glass cup",
        "Glass jar",
        "Other glass",
    ],
    "hazardous": [
        "Battery",
        "Syringe",
        "Medical waste",
        "Light bulb",
        "Chemical",
    ],
}

# ── Skip these — too ambiguous to train on ─────────────
SKIP = ["Unlabeled litter", "Scrap metal", "Rope & strings","Shoe"]

# ── Build flat lookup: taco_name → swos_class ──────────
flat_map = {}
for swos_class, names in REMAP.items():
    for name in names:
        flat_map[name.lower().strip()] = swos_class

CLASSES      = ["plastic", "organic", "metal", "glass", "hazardous"]
class_to_idx = {c: i for i, c in enumerate(CLASSES)}

# ── Create output folders ──────────────────────────────
for split in ["train", "val", "test"]:
    (OUTPUT_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)

# ── Load TACO ──────────────────────────────────────────
with open(TACO_JSON) as f:
    taco = json.load(f)

cat_id_to_swos = {}
unmapped = []
for cat in taco["categories"]:
    name   = cat["name"].lower().strip()
    mapped = flat_map.get(name)
    if mapped:
        cat_id_to_swos[cat["id"]] = mapped
    elif cat["name"] not in SKIP:
        unmapped.append(cat["name"])

if unmapped:
    print(f"\n⚠️  Still unmapped ({len(unmapped)}) — review these:")
    for u in unmapped:
        print(f"   - {u}")

# ── Build image_id → split mapping (80/15/5) ──────────
all_image_ids = [img["id"] for img in taco["images"]]
random.seed(42)
random.shuffle(all_image_ids)
n = len(all_image_ids)
train_ids = set(all_image_ids[:int(n * 0.80)])
val_ids   = set(all_image_ids[int(n * 0.80):int(n * 0.95)])
test_ids  = set(all_image_ids[int(n * 0.95):])

def get_split(image_id):
    if image_id in train_ids: return "train"
    if image_id in val_ids:   return "val"
    return "test"

# ── Image lookup ──────────────────────────────────────
img_lookup = {img["id"]: img for img in taco["images"]}

# ── Process annotations → YOLO labels ─────────────────
counts  = {c: 0 for c in CLASSES}
skipped = 0
copied_images = set()

for ann in taco["annotations"]:
    swos_class = cat_id_to_swos.get(ann["category_id"])
    if not swos_class:
        skipped += 1
        continue

    img_info = img_lookup[ann["image_id"]]
    img_w    = img_info["width"]
    img_h    = img_info["height"]
    x, y, w, h = ann["bbox"]

    # YOLO normalised format
    cx = (x + w / 2) / img_w
    cy = (y + h / 2) / img_h
    nw = w / img_w
    nh = h / img_h

    # Skip invalid boxes
    if nw <= 0 or nh <= 0:
        skipped += 1
        continue

    class_idx  = class_to_idx[swos_class]
    split      = get_split(ann["image_id"])
    img_stem   = Path(img_info["file_name"]).stem

    # Write label line
    label_path = OUTPUT_DIR / "labels" / split / f"{img_stem}.txt"
    with open(label_path, "a") as lf:
        lf.write(f"{class_idx} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}\n")

    # Copy image once
    if ann["image_id"] not in copied_images:
        src = IMAGES_DIR / img_info["file_name"]
        dst = OUTPUT_DIR / "images" / split / Path(img_info["file_name"]).name
        if src.exists():
            shutil.copy2(src, dst)
        copied_images.add(ann["image_id"])

    counts[swos_class] += 1

# ── Print results ─────────────────────────────────────
print("\n✅  Class distribution after remap:")
print("-" * 45)
total = sum(counts.values())
for cls, cnt in counts.items():
    bar  = "█" * (cnt // 15)
    pct  = (cnt / total * 100) if total else 0
    flag = " ⚠️  NEEDS MORE DATA" if cnt < 50 else ""
    print(f"  {cls:<12} {cnt:>4} samples  {pct:4.1f}%  {bar}{flag}")

print(f"\n  Total usable:  {total}")
print(f"  Skipped:       {skipped}")
print(f"\n  Train images:  {len(train_ids)}")
print(f"  Val images:    {len(val_ids)}")
print(f"  Test images:   {len(test_ids)}")