import os
from pathlib import Path
import re
import shutil

BASE_DIR = Path(r"C:\Users\BalasubramanianPG\Music\stratascratch_questions\StrataScratch_Full_DB")


def extract_yaml_properties(md_path):
    """
    Extract 'id' and 'difficulty' from YAML front matter.
    Assumes front matter is at the top of the file between lines containing only '---'.
    """
    id_value = None
    difficulty_value = None

    with md_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    # Check if file starts with YAML front matter
    if not lines or not lines[0].strip().startswith("---"):
        return None, None

    # Find the end of the YAML block
    yaml_lines = []
    # Start from line 1 because line 0 is '---'
    for line in lines[1:]:
        if line.strip().startswith("---"):
            break
        yaml_lines.append(line.rstrip("\n"))

    # Very simple "key: value" parser
    for line in yaml_lines:
        # Ignore empty or comment lines
        if not line.strip() or line.strip().startswith("#"):
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip().strip('"').strip("'")

        if key == "id":
            id_value = value
        elif key == "difficulty":
            difficulty_value = value

    return id_value, difficulty_value


def make_title_from_filename(stem):
    """
    Convert 'homework-results' or 'homework_results' into 'Homework Results'.
    Does not try to strip existing numeric prefixes.
    """
    # Replace hyphens and underscores with spaces
    title = re.sub(r"[-_]+", " ", stem)
    # Collapse multiple spaces
    title = re.sub(r"\s+", " ", title).strip()
    # Title case
    return title.title()


def main():
    if not BASE_DIR.exists():
        print(f"Base directory does not exist: {BASE_DIR}")
        return

    # Get all markdown files only in this folder (non recursive)
    md_files = list(BASE_DIR.glob("*.md"))

    for md_path in md_files:
        print(f"Processing: {md_path.name}")

        file_stem = md_path.stem

        # 1. Extract id and difficulty from YAML
        id_value, difficulty_value = extract_yaml_properties(md_path)

        if not id_value:
            print(f"  Skipping (no 'id' found in YAML): {md_path.name}")
            continue

        if not difficulty_value:
            print(f"  Skipping (no 'difficulty' found in YAML): {md_path.name}")
            continue

        # 2. Build new title part from current filename
        title_part = make_title_from_filename(file_stem)

        # 3. Build new file name: "ID. Title.md"
        new_filename = f"{id_value}. {title_part}.md"

        # 4. Normalise difficulty to folder name, e.g. "easy" -> "Easy"
        difficulty_folder_name = difficulty_value.strip().title()
        difficulty_dir = BASE_DIR / difficulty_folder_name
        difficulty_dir.mkdir(exist_ok=True)

        new_path = difficulty_dir / new_filename

        # 5. Move and rename the file
        print(f"  -> {new_path}")
        shutil.move(str(md_path), str(new_path))

    print("Done.")


if __name__ == "__main__":
    main()
