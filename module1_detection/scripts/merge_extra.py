import shutil
import yaml
from pathlib import Path

EXTRA_DIR    = Path(r"C:\SWOS\module1_detection\data\roboflow_extra")
WASTE_DATASET= Path(r"C:\SWOS\module1_detection\data\waste_dataset")

CLASS_MAP = {
    "plastic"  : 0,
    "organic"  : 1,
    "metal"    : 2,
    "glass"    : 3,
}

# Keywords to match class names from each dataset
CLASS_KEYWORDS = {
    "plastic" : ["plastic", "bottle", "wrapper", "container", "bag", "film"],
    "organic" : ["organic", "food", "waste", "paper", "cardboard", "carton"],
    "metal"   : ["metal", "can", "tin", "aluminium", "steel"],
    "glass"   : ["glass", "bottle"],
}

total_added = {c: 0 for c in CLASS_MAP}

for swos_class, swos_idx in CLASS_MAP.items():
    src_base = EXTRA_DIR / swos_class
    if not src_base.exists():
        print(f"⚠️  Folder not found: {src_base}")
        continue

    # Read data.yaml to get class names
    yaml_path = src_base / "data.yaml"
    if not yaml_path.exists():
        print(f"⚠️  No data.yaml in {src_base}")
        continue

    with open(yaml_path) as f:
        meta = yaml.safe_load(f)

    src_names = meta.get("names", [])
    if isinstance(src_names, dict):
        src_names = list(src_names.values())

    print(f"\n📁 {swos_class.upper()} dataset classes: {src_names}")

    # Find which source class indices match our swos class
    keywords      = CLASS_KEYWORDS[swos_class]
    valid_indices = []
    for i, name in enumerate(src_names):
        if any(kw in name.lower() for kw in keywords):
            valid_indices.append(i)
            print(f"   ✅ Mapping source class {i} '{name}' → {swos_class}")

    if not valid_indices:
        print(f"   ⚠️  No matching classes found — mapping ALL classes to {swos_class}")
        valid_indices = list(range(len(src_names)))

    # Copy images + remap labels
    for split, src_split in [("train","train"), ("val","valid"), ("test","test")]:
        src_images = src_base / src_split / "images"
        src_labels = src_base / src_split / "labels"
        dst_images = WASTE_DATASET / "images" / split
        dst_labels = WASTE_DATASET / "labels" / split

        if not src_images.exists():
            continue

        copied = 0
        for lf in src_labels.glob("*.txt"):
            lines     = lf.read_text().strip().splitlines()
            new_lines = []

            for line in lines:
                if not line.strip():
                    continue
                parts    = line.split()
                class_id = int(parts[0])
                if class_id in valid_indices:
                    new_lines.append(f"{swos_idx} {' '.join(parts[1:])}")

            if not new_lines:
                continue

            # Find image
            img_file = None
            for ext in [".jpg", ".jpeg", ".png"]:
                candidate = src_images / f"{lf.stem}{ext}"
                if candidate.exists():
                    img_file = candidate
                    break

            if not img_file:
                continue

            # Save with unique prefix
            new_name = f"{swos_class}_{lf.stem}"
            shutil.copy2(img_file, dst_images / f"{new_name}{img_file.suffix}")
            (dst_labels / f"{new_name}.txt").write_text("\n".join(new_lines))
            copied += 1

        total_added[swos_class] += copied
        print(f"   {split}: +{copied}")

print("\n" + "=" * 45)
print("MERGE COMPLETE")
print("=" * 45)
for cls, cnt in total_added.items():
    print(f"  {cls:<12} +{cnt} images added")
print("\nNow re-zip waste_dataset and retrain on Colab!")