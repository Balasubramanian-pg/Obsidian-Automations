import os
import re
import shutil
from collections import defaultdict
from pathlib import Path

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------
SOURCE_ROOT = r"C:\Users\BalasubramanianPG\Videos\Obsidian Vault\3. Interview Prep\Stratascratch"
TARGET_ROOT = r"C:\Users\BalasubramanianPG\Videos\Organized_By_Patterns"

DIFFICULTY_OFFSET = {
    "Easy": 1,
    "Medium": 2,
    "Hard": 3,
    "Advanced": 4
}

# Canonical family → base chapter
FAMILY_PATTERN_MAP = {
    # Basics
    "Data Retrieval Basics": 10,
    "Filtering Data": 10,
    "Boolean Indexing": 10,
    "Column Manipulation": 10,
    "DataFrame Operations": 10,
    "DataFrame Creation": 10,
    "Data Cleaning": 10,
    "Conditional Logic": 10,
    "Combining": 10,
    # Aggregations
    "Aggregate Functions": 20,
    "Aggregation Methods": 20,
    "Aggregations": 20,
    "Distinct Counts": 20,
    "Array Operation": 20,
    # Advanced
    "Window Functions": 30,
    "Advanced Joins": 30,
}

UNKNOWN_BASE = 99

# -------------------------------------------------
# ENABLE LONG PATH SUPPORT
# -------------------------------------------------
def enable_long_paths(path):
    """Prefix path with extended-length path namespace to bypass 260 char limit"""
    if os.name == 'nt':
        abs_path = os.path.abspath(path)
        if not abs_path.startswith('\\\\?\\'):
            if abs_path.startswith('\\\\'):
                # UNC path
                return '\\\\?\\UNC\\' + abs_path[2:]
            else:
                # Regular path
                return '\\\\?\\' + abs_path
    return path

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def clean_yaml_value(value: str) -> str:
    value = value.strip().strip('"').strip("'")
    value = value.replace('\\"', '').replace("\\'", '')
    return value

def extract_yaml(content: str) -> dict:
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    yaml_block = match.group(1)
    
    def find(key):
        m = re.search(rf'^{key}:\s*(.+)$', yaml_block, re.MULTILINE)
        return clean_yaml_value(m.group(1)) if m else None
    
    return {
        "family": find("topic_family"),
        "function": find("topic_functions") or find("topic_function")
    }

def infer_difficulty(path: str) -> str:
    for part in path.split(os.sep):
        if part in DIFFICULTY_OFFSET:
            return part
    return "Unknown"

def to_title_case(text: str) -> str:
    """Convert text to Title Case, removing underscores, hyphens, and illegal chars"""
    # Remove illegal Windows filename characters: \ / : * ? " < > | ( )
    illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '(', ')']
    for char in illegal_chars:
        text = text.replace(char, '')
    
    # Replace underscores and hyphens with spaces
    text = text.replace('_', ' ').replace('-', ' ')
    
    # Title case each word
    return ' '.join(word.capitalize() for word in text.split())

# -------------------------------------------------
# MAIN PROCESS
# -------------------------------------------------
file_groups = defaultdict(list)

print("📂 Scanning source files...")
for root, _, files in os.walk(SOURCE_ROOT):
    for file in files:
        if not file.endswith(".md"):
            continue
        
        full_path = os.path.join(root, file)
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Could not read: {file}")
            continue
        
        meta = extract_yaml(content)
        family = meta.get("family") or "UNKNOWN_FAMILY"
        function = meta.get("function") or "UNKNOWN_FUNCTION"
        difficulty = infer_difficulty(root)
        
        base = FAMILY_PATTERN_MAP.get(family, UNKNOWN_BASE)
        offset = DIFFICULTY_OFFSET.get(difficulty, 0)
        chapter_number = base + offset if base != UNKNOWN_BASE else UNKNOWN_BASE
        
        file_groups[(chapter_number, family, function)].append(full_path)

# -------------------------------------------------
# RENUMBER CHAPTERS SEQUENTIALLY
# -------------------------------------------------
unique_chapters = sorted(set(ch for ch, _, _ in file_groups.keys()))
chapter_map = {old: new for new, old in enumerate(unique_chapters, start=1)}

# Create restructured data with sub-chapters
restructured = defaultdict(lambda: defaultdict(list))

for (old_chapter, family, function), files in file_groups.items():
    new_chapter = chapter_map[old_chapter]
    restructured[new_chapter][(family, function)] = files

# -------------------------------------------------
# FILE ORGANIZATION WITH LONG PATH SUPPORT
# -------------------------------------------------
target_root_long = enable_long_paths(TARGET_ROOT)
Path(TARGET_ROOT).mkdir(parents=True, exist_ok=True)

print("\n📁 Creating folder structure...")

for chapter_num in sorted(restructured.keys()):
    subfamilies = restructured[chapter_num]
    
    chapter_dir_name = f"Chapter {chapter_num}"
    chapter_path = os.path.join(TARGET_ROOT, chapter_dir_name)
    chapter_path_long = enable_long_paths(chapter_path)
    
    Path(chapter_path).mkdir(parents=True, exist_ok=True)
    
    for sub_num, ((family, function), files) in enumerate(sorted(subfamilies.items()), start=1):
        subchapter_name = f"{chapter_num}.{sub_num} {to_title_case(family)}"
        function_name = to_title_case(function)
        
        dest_dir = os.path.join(chapter_path, subchapter_name, function_name)
        dest_dir_long = enable_long_paths(dest_dir)
        
        try:
            Path(dest_dir).mkdir(parents=True, exist_ok=True)
            
            copied = 0
            for src in files:
                src_long = enable_long_paths(src)
                dest_file = os.path.join(dest_dir, os.path.basename(src))
                dest_file_long = enable_long_paths(dest_file)
                
                shutil.copy2(src_long, dest_file_long)
                copied += 1
            
            print(f"✓ {subchapter_name} → {function_name} ({copied} files)")
            
        except Exception as e:
            print(f"✗ ERROR: {subchapter_name} → {function_name}")
            print(f"   {str(e)}")

print("\n✅ Organization complete!")
print(f"📁 Output: {TARGET_ROOT}")