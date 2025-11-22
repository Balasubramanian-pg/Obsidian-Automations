import json
import random
from pathlib import Path

# Paths
VAULT_PATH = Path(r"C:\Users\ASUS\Videos\AnyDesk\Balasubramanian PG")
ARCHIVES = VAULT_PATH / "09. Archives"
ICON_FOLDER_DATA = VAULT_PATH / ".obsidian" / "plugins" / "obsidian-icon-folder" / "data.json"

# Your simple icons directory
SIMPLE_ICONS_DIR = VAULT_PATH / ".obsidian" / "icons" / "simple-icons" / "simple-icons-11.10.0" / "icons"

# Load SVG file names for Simple Icons
svg_files = list(SIMPLE_ICONS_DIR.glob("*.svg"))
simple_icons = [svg.stem for svg in svg_files]

print("Loaded icons:", len(simple_icons))
if not simple_icons:
    raise Exception("No icons found. Check SIMPLE_ICONS_DIR path.")

# Load icon-folder plugin data.json
with open(ICON_FOLDER_DATA, "r", encoding="utf-8") as f:
    data = json.load(f)

# Ensure required keys exist
if "files" not in data:
    data["files"] = {}

updated_count = 0

# Assign random icons to files in Archives
for file in ARCHIVES.rglob("*.md"):
    rel_path = str(file.relative_to(VAULT_PATH)).replace("\\", "/")

    chosen = random.choice(simple_icons)

    data["files"][rel_path] = {
        "icon": chosen,
        "color": None,
        "iconPack": "simple-icons"
    }

    updated_count += 1
    print(f"{rel_path} → {chosen}")

# Save updated data.json
with open(ICON_FOLDER_DATA, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"\nDone. Updated icons for {updated_count} files.")
print("Reload Obsidian or toggle Icon Folder plugin to see changes.")
