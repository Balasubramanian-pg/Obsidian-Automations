import os
import shutil
from pathlib import Path
import yaml

# =========================
# CONFIG
# =========================

VAULT_PATH = r"C:\Users\ASUS\Videos\AnyDesk\Balasubramanian PG"
DRY_RUN = False          # Set to False to actually move + rewrite
CREATE_BACKUP = True    # Backup vault before mutating

vault = Path(VAULT_PATH)

GLOBAL_FOLDERS = {
    "Personal":        "01. Personal",
    "Work":            "02. Work",
    "Interview Prep":  "03. Interview Prep",
    "Learning":        "04. Learning",
    "Projects":        "05. Projects",
    "SOP":             "06. SOP",
    "Templates":       "07. Templates",
    "Assets":          "08. Assets",
    "Archives":        "09. Archives",
}

# Keywords to classify top-level folders (Option A)
AREA_KEYWORDS = {
    "Interview Prep": [
        "interview", "leetcode", "coding", "dsa", "sql interview",
        "question bank", "mcq"
    ],
    "Learning": [
        "course", "certification", "pl-300", "pl - 300", "pl-400",
        "pl - 400", "learning", "udemy", "coursera"
    ],
    "Work": [
        "client", "master prompts", "agile", "scrum", "kanban",
        "delivery", "consulting", "flipcarbon", "finance", "cfo",
        "chro", "ops", "operations", "marketing"
    ],
    "Projects": [
        "project", "projects", "case study"
    ],
    "SOP": [
        "sop", "standard operating", "process", "procedure"
    ],
    "Templates": [
        "template", "templates", "snippet", "snippets"
    ],
    "Assets": [
        "assets", "images", "icons", "img", "media"
    ],
    "Personal": [
        "journal", "daily", "personal", "life", "thoughts", "バラスブラマニアン"
    ],
}

# Defaults for Type based on Area
AREA_TYPE_DEFAULT = {
    "Personal":       "Personal Note",
    "Work":           "Work Note",
    "Interview Prep": "Interview Question",
    "Learning":       "Learning Note",
    "Projects":       "Project",
    "SOP":            "SOP Document",
    "Templates":      "Template",
    "Assets":         "Asset",
    "Archives":       "Archive Note",
}

GLOBAL_FIELDS = ["Title", "Created", "Updated", "Tags", "Type", "Status", "Area", "Topic", "Source"]

INTERVIEW_FIELDS = ["Difficulty", "Company", "Question Link", "Category", "Sub Category", "Date"]
LEARNING_FIELDS = ["Course", "Module", "Duration", "Date"]
SOP_FIELDS = ["Document Type", "Parent SOP", "Last Reviewed", "Next Review", "Owner"]


# =========================
# UTILITIES
# =========================

def title_case_property(key: str) -> str:
    """
    Normalize YAML property names:
    - snake_case / camelCase / lowercase / uppercase -> Title Case with spaces
    - No underscores.
    """
    original = key.strip()

    # If already looks like "Title Case" with spaces, keep as-is
    if " " in original and original == original.title():
        return original

    k = original.replace("_", " ")

    # Insert spaces before camelCase transitions: createdDate -> created Date
    out = []
    prev_lower = False
    for ch in k:
        if prev_lower and ch.isupper():
            out.append(" ")
        out.append(ch)
        prev_lower = ch.islower()
    k = "".join(out)

    k = " ".join(k.split())
    return k.title()


def classify_area_from_name(name: str) -> str:
    """
    Use folder name (or path snippet) to guess which high-level Area it belongs to.
    Fallback: Archives.
    """
    lower = name.lower()

    for area, keywords in AREA_KEYWORDS.items():
        for kw in keywords:
            if kw in lower:
                return area
    # If nothing matches, choose Archives
    return "Archives"


def read_note_frontmatter(path: Path):
    """
    Returns (meta_dict, body_text).
    If no frontmatter, meta_dict = {} and body is full text.
    """
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines(keepends=True)

    if not lines or not lines[0].strip().startswith("---"):
        return {}, text

    front_lines = []
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip().startswith("---"):
            end_idx = i
            break
        front_lines.append(line)

    if end_idx is None:
        # malformed frontmatter
        return {}, text

    body = "".join(lines[end_idx+1:])
    try:
        meta = yaml.safe_load("".join(front_lines)) or {}
        if not isinstance(meta, dict):
            meta = {}
    except Exception:
        meta = {}

    return meta, body


def write_note_frontmatter(path: Path, meta: dict, body: str):
    """
    Overwrites file with YAML + body.
    """
    yaml_str = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip()
    new_text = "---\n" + yaml_str + "\n---\n" + body
    path.write_text(new_text, encoding="utf-8")


# =========================
# STEP 1: BACKUP (optional)
# =========================

if CREATE_BACKUP and not DRY_RUN:
    backup_path = vault.parent / (vault.name + "_backup_before_migration")
    if not backup_path.exists():
        print(f"Creating backup at: {backup_path}")
        shutil.copytree(vault, backup_path)
    else:
        print(f"Backup already exists at: {backup_path}")


# =========================
# STEP 2: CLASSIFY TOP-LEVEL FOLDERS
# =========================

# Find top-level folders and root .md files
top_level_dirs = set()
root_md_files = []

for p in vault.iterdir():
    if p.is_dir():
        top_level_dirs.add(p.name)
    elif p.is_file() and p.suffix.lower() == ".md":
        root_md_files.append(p)

folder_area_map = {}

for dirname in sorted(top_level_dirs):
    area = classify_area_from_name(dirname)
    folder_area_map[dirname] = area

print("Top-level folder → Area mapping (DRY preview):")
for d, a in folder_area_map.items():
    print(f"  {d}  →  {a}  →  {GLOBAL_FOLDERS[a]}")

if DRY_RUN:
    print("\n[DRY RUN] No folders moved yet.")
else:
    # Ensure global root folders exist
    for area, folder_name in GLOBAL_FOLDERS.items():
        (vault / folder_name).mkdir(exist_ok=True)

    # Move top-level folders into their global area folders
    for dirname, area in folder_area_map.items():
        src = vault / dirname
        dst_root = vault / GLOBAL_FOLDERS[area]
        dst_root.mkdir(exist_ok=True)
        dst = dst_root / dirname

        if dst.exists():
            print(f"WARNING: Destination already exists, skipping move: {dst}")
            continue

        print(f"Moving {src} -> {dst}")
        shutil.move(str(src), str(dst))

    # Handle root md files (no parent folder)
    for f in root_md_files:
        area = classify_area_from_name(f.stem)
        dst_root = vault / GLOBAL_FOLDERS[area]
        dst_root.mkdir(exist_ok=True)
        dst = dst_root / f.name

        if dst.exists():
            print(f"WARNING: Destination already exists for root file, skipping: {dst}")
            continue

        print(f"Moving root file {f} -> {dst}")
        shutil.move(str(f), str(dst))


# =========================
# STEP 3: REWRITE YAML FRONTMATTER
# =========================

def get_area_for_file(rel_path: Path) -> str:
    """
    After moves: Area is determined by the global folder name in path.
    Example: 03. Interview Prep/SQL Interview Prep/... -> Interview Prep
    """
    if len(rel_path.parts) == 0:
        return "Archives"

    top = rel_path.parts[0]
    # Try to match by GLOBAL_FOLDERS values
    for area, folder_name in GLOBAL_FOLDERS.items():
        if top == folder_name:
            return area

    # Fallback: classify by path text
    return classify_area_from_name(str(rel_path))


def normalize_meta_keys(meta: dict) -> dict:
    normalized = {}
    for k, v in meta.items():
        new_k = title_case_property(str(k))
        if new_k not in normalized:
            normalized[new_k] = v
        else:
            # If collision, keep the first non-empty-ish value
            if normalized[new_k] in [None, "", []] and v not in [None, "", []]:
                normalized[new_k] = v
    return normalized


def enrich_meta(meta: dict, file_path: Path, rel_path: Path) -> dict:
    meta = normalize_meta_keys(meta)

    area = get_area_for_file(rel_path)
    # Global fields
    if "Title" not in meta or not meta["Title"]:
        meta["Title"] = file_path.stem

    if "Area" not in meta or not meta["Area"]:
        meta["Area"] = area

    if "Type" not in meta or not meta["Type"]:
        meta["Type"] = AREA_TYPE_DEFAULT.get(area, "Note")

    if "Status" not in meta or not meta["Status"]:
        meta["Status"] = "Draft"

    if "Source" not in meta or not meta["Source"]:
        meta["Source"] = str(rel_path).replace("\\", "/")

    # Ensure all global fields exist (but do not overwrite if present)
    for field in GLOBAL_FIELDS:
        if field not in meta:
            meta[field] = "" if field not in ["Title", "Area", "Type", "Status", "Source"] else meta.get(field, "")

    # Area-specific fields
    if area == "Interview Prep":
        for f in INTERVIEW_FIELDS:
            if f not in meta:
                meta[f] = ""
    elif area == "Learning":
        for f in LEARNING_FIELDS:
            if f not in meta:
                meta[f] = ""
    elif area == "SOP":
        for f in SOP_FIELDS:
            if f not in meta:
                meta[f] = ""

    return meta


# Walk all md files in the vault (after potential move)
all_md_files = list(vault.rglob("*.md"))
print(f"\nFound {len(all_md_files)} markdown files for YAML normalization.")

for path in all_md_files:
    rel = path.relative_to(vault)
    meta, body = read_note_frontmatter(path)

    new_meta = enrich_meta(meta, path, rel)

    if DRY_RUN:
        # Preview for first few files only
        if "preview_count" not in globals():
            preview_count = 0
        if preview_count < 10:
            print(f"\n[DRY RUN] {rel}")
            print("Old keys:", sorted(meta.keys()))
            print("New keys:", sorted(new_meta.keys()))
            preview_count += 1
        continue
    else:
        write_note_frontmatter(path, new_meta, body)

print("\nDone. DRY_RUN =", DRY_RUN)
print("If everything looks good, set DRY_RUN = False and re-run.")
