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

# 1. DEFINE CANONICAL FAMILIES (Group synonyms together)
# Maps 'Raw Metadata Value' -> 'Clean Family Name'
FAMILY_MAPPING = {
    # Basics Group
    "Data Retrieval Basics": "Data Retrieval Basics",
    "Filtering Data": "Data Retrieval Basics",
    "Boolean Indexing": "Data Retrieval Basics",
    "Column Manipulation": "Data Retrieval Basics",
    "DataFrame Operations": "Data Retrieval Basics",
    "DataFrame Creation": "Data Retrieval Basics",
    "Data Cleaning": "Data Retrieval Basics",
    "Conditional Logic": "Data Retrieval Basics",
    "Combining": "Data Retrieval Basics",
    
    # Aggregation Group
    "Aggregate Functions": "Aggregate Functions",
    "Aggregation Methods": "Aggregate Functions",
    "Aggregations": "Aggregate Functions",
    "Distinct Counts": "Aggregate Functions",
    "Array Operation": "Aggregate Functions",
    
    # Advanced Group
    "Window Functions": "Window Functions",
    "Advanced Joins": "Window Functions", # Assuming you want joins here, or separate
}

# 2. DEFINE SORT ORDER
# Chapters will appear in this order of Families...
FAMILY_ORDER = [
    "Data Retrieval Basics",
    "Aggregate Functions",
    "Window Functions"
]

# ...and within families, in this order of Difficulty
DIFFICULTY_ORDER = ["Easy", "Medium", "Hard", "Advanced", "Unknown"]

# -------------------------------------------------
# LONG PATH SUPPORT (WINDOWS)
# -------------------------------------------------
def enable_long_paths(path):
    if os.name == 'nt':
        abs_path = os.path.abspath(path)
        if not abs_path.startswith('\\\\?\\'):
            if abs_path.startswith('\\\\'):
                return '\\\\?\\UNC\\' + abs_path[2:]
            return '\\\\?\\' + abs_path
    return path

# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def clean_text(text):
    if not text: return "Unknown"
    # Remove bad characters for filenames
    text = re.sub(r'[\\/*?:"<>|]', '', text)
    return text.strip()

def extract_metadata(content):
    """Extract topic_family and topic_function from YAML"""
    meta = {}
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    
    if match:
        yaml_block = match.group(1)
        # Helper to regex find specific keys
        def find_key(keys):
            for k in keys:
                m = re.search(rf'^{k}:\s*(.+)$', yaml_block, re.MULTILINE)
                if m: 
                    val = m.group(1).strip().strip('"\'')
                    return val
            return None

        meta['family'] = find_key(['topic_family'])
        meta['function'] = find_key(['topic_function', 'topic_functions'])
    
    return meta

def get_difficulty(path):
    """Check path folders for difficulty keywords"""
    parts = path.split(os.sep)
    for d in DIFFICULTY_ORDER:
        if d in parts:
            return d
    return "Unknown"

# -------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------
def main():
    print(f"🚀 Starting organization...")
    print(f"📂 Source: {SOURCE_ROOT}")
    
    # Data Structure: 
    # structured_data[(canonical_family, difficulty)][function_name] = [list_of_files]
    structured_data = defaultdict(lambda: defaultdict(list))
    
    total_files = 0
    skipped_files = 0

    # --- PHASE 1: SCAN AND GROUP ---
    for root, dirs, files in os.walk(SOURCE_ROOT):
        for file in files:
            if not file.endswith('.md'):
                continue
            
            total_files += 1
            full_path = os.path.join(root, file)
            
            # Read Content
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                print(f"⚠️ Cannot read: {file}")
                skipped_files += 1
                continue
            
            # Extract Meta
            meta = extract_metadata(content)
            raw_family = meta.get('family')
            raw_function = meta.get('function') or "General"
            
            # Determine Difficulty
            difficulty = get_difficulty(root)
            
            # Normalize Family
            canonical_family = FAMILY_MAPPING.get(raw_family, "Other")
            
            # Clean names for folder creation
            clean_func = clean_text(raw_function)
            
            # Group it!
            # The key determines what defines a "Chapter"
            chapter_key = (canonical_family, difficulty)
            structured_data[chapter_key][clean_func].append(full_path)

    # --- PHASE 2: SORT CHAPTERS ---
    # Convert dict keys to list and sort based on Configuration Order
    all_chapter_keys = list(structured_data.keys())
    
    def sort_logic(key):
        fam, diff = key
        # Get index from config lists, default to high number if not found (put at end)
        fam_idx = FAMILY_ORDER.index(fam) if fam in FAMILY_ORDER else 999
        diff_idx = DIFFICULTY_ORDER.index(diff) if diff in DIFFICULTY_ORDER else 999
        return (fam_idx, diff_idx)

    sorted_chapters = sorted(all_chapter_keys, key=sort_logic)

    # --- PHASE 3: CREATE STRUCTURE ---
    if os.path.exists(TARGET_ROOT):
        print("🗑️  Cleaning previous target folder (Safety: Manual check recommended in real run)")
        # shutil.rmtree(TARGET_ROOT) # Uncomment if you want auto-delete
    
    Path(TARGET_ROOT).mkdir(parents=True, exist_ok=True)
    
    chapter_counter = 1
    
    for (family, diff) in sorted_chapters:
        # Define Chapter Name
        # Ex: "Chapter 1 - Aggregate Functions (Easy)"
        chapter_folder_name = f"Chapter {chapter_counter} - {family} ({diff})"
        chapter_path = os.path.join(TARGET_ROOT, chapter_folder_name)
        
        functions_map = structured_data[(family, diff)]
        
        # Sort sub-chapters (Functions) alphabetically
        sorted_functions = sorted(functions_map.keys())
        
        # Track if this chapter actually gets created
        files_moved_in_chapter = 0
        
        sub_counter = 1
        for func_name in sorted_functions:
            file_list = functions_map[func_name]
            
            # Define Sub-Chapter Name
            # Ex: "1.1 Sum"
            sub_folder_name = f"{chapter_counter}.{sub_counter} {func_name}"
            final_dest_dir = os.path.join(chapter_path, sub_folder_name)
            
            # Create Folder (with long path support)
            Path(enable_long_paths(final_dest_dir)).mkdir(parents=True, exist_ok=True)
            
            # Copy Files
            for src_file in file_list:
                file_name = os.path.basename(src_file)
                dst_file = os.path.join(final_dest_dir, file_name)
                
                try:
                    shutil.copy2(enable_long_paths(src_file), enable_long_paths(dst_file))
                    files_moved_in_chapter += 1
                except Exception as e:
                    print(f"❌ Error copying {file_name}: {e}")
            
            sub_counter += 1
        
        if files_moved_in_chapter > 0:
            print(f"✅ Created: {chapter_folder_name} ({files_moved_in_chapter} files)")
            chapter_counter += 1

    print("\n" + "="*50)
    print("DONE!")
    print(f"Total MD Files Processed: {total_files}")
    print(f"Skipped/Errors: {skipped_files}")
    print(f"Location: {TARGET_ROOT}")

if __name__ == "__main__":
    main()