import shutil
import os
from pathlib import Path
import random

# ── Paths ──────────────────────────────────────────────
WASTE_DATASET = Path(r"C:\SWOS\module1_detection\data\waste_dataset")
ROBOFLOW_DIR  = Path(r"C:\SWOS\module1_detection\data\roboflow_hazardous")

# Class index for hazardous in YOUR dataset = 4
HAZARDOUS_IDX = 4

def copy_as_hazardous(src_images, src_labels, split, class_indices):
    """
    Copy images + rewrite labels mapping 
    source class indices → our hazardous class (4)
    """
    dst_images = WASTE_DATASET / "images" / split
    dst_labels = WASTE_DATASET / "labels" / split
    
    copied = 0
    skipped = 0
    
    label_files = list(src_labels.glob("*.txt"))
    
    for lf in label_files:
        lines     = lf.read_text().strip().splitlines()
        new_lines = []
        
        for line in lines:
            if not line.strip():
                continue
            parts    = line.split()
            class_id = int(parts[0])
            
            # Only keep lines whose class is in our accepted list
            if class_id in class_indices:
                # Remap to hazardous = 4
                new_line = f"4 {' '.join(parts[1:])}"
                new_lines.append(new_line)
        
        if not new_lines:
            skipped += 1
            continue
        
        # Find matching image
        img_stem = lf.stem
        img_file = None
        for ext in [".jpg", ".jpeg", ".png"]:
            candidate = src_images / f"{img_stem}{ext}"
            if candidate.exists():
                img_file = candidate
                break
        
        if not img_file:
            skipped += 1
            continue
        
        # Copy image with unique name to avoid conflicts
        new_name = f"haz_{img_stem}"
        shutil.copy2(img_file, dst_images / f"{new_name}{img_file.suffix}")
        
        # Write remapped label
        (dst_labels / f"{new_name}.txt").write_text("\n".join(new_lines))
        copied += 1
    
    return copied, skipped


total_added = 0

# ── Will fill these paths after you send yaml contents ──
DATASETS = [
    {
        "name": "capy",
        "base": ROBOFLOW_DIR / "capy",
        # class indices that mean hazardous in THIS dataset
        # WE FILL THIS AFTER SEEING data.yaml
        "hazardous_classes": [0],
    },
    {
        "name": "mysterious", 
        "base": ROBOFLOW_DIR / "mysterious",
        "hazardous_classes": [0],
    },
]

for ds in DATASETS:
    # Find the actual subfolder with train/valid/test
    subfolders = [f for f in ds["base"].iterdir() if f.is_dir()]
    if not subfolders:
        print(f"⚠️  No subfolder found in {ds['base']}")
        continue
    base = subfolders[0]
    
    print(f"\nProcessing: {ds['name']}")
    
    for split, src_split in [("train","train"), ("val","valid"), ("test","test")]:
        src_images = base / src_split / "images"
        src_labels = base / src_split / "labels"
        
        if not src_images.exists():
            continue
            
        added, skipped = copy_as_hazardous(
            src_images, src_labels, 
            split, ds["hazardous_classes"]
        )
        print(f"  {split}: +{added} images  (skipped {skipped})")
        total_added += added

print(f"\n✅ Total hazardous samples added: {total_added}")
print("Now re-run remap_categories.py to see updated distribution")