import os
import shutil
import pandas as pd
from pathlib import Path
import json

# ==========================================
# 1. SETUP AND CONFIGURATION
# ==========================================
directory_path = r"C:\Users\BalasubramanianPG\Videos\Obsidian Vault\Power BI\Query Langauges\DAX"
base_path = Path(directory_path)

# Verify directory
if not base_path.exists():
    raise FileNotFoundError(f"Directory not found: {directory_path}")

print(f"Working in: {base_path}")

# ==========================================
# 2. CATEGORIZATION DICTIONARY (Collapsed for brevity, using yours)
# ==========================================
# [Paste your large categorization dictionary here if not already in memory]
# Assuming 'categorization' variable exists from your previous code. 
# If you are running this as a fresh script, copy your dictionary back in here.
# For safety, I will rely on the variable 'categorization' being present.
if 'categorization' not in locals():
    print("CRITICAL: Categorization dictionary missing. Please ensure the dictionary is defined.")
    # Quick fix to prevent crash if running this standalone without the dict
    categorization = {} 

# ==========================================
# 3. FIXED ANALYSIS FUNCTION (Handles Case Sensitivity)
# ==========================================
def auto_categorize(filename):
    """Fallback categorization logic"""
    filename_lower = filename.lower()
    if "dax-" in filename_lower: return ("Concepts", "Miscellaneous")
    if "-functions-dax" in filename_lower: return ("Categories-Overview", None)
    if any(k in filename_lower for k in ["date", "time", "year", "month"]): return ("Core Functions", "Date-Time")
    if any(k in filename_lower for k in ["sum", "count", "avg", "min", "max"]): return ("Core Functions", "Aggregation")
    if any(k in filename_lower for k in ["filter", "all", "select"]): return ("Core Functions", "Filter")
    return ("Core Functions", "Other")

def analyze_files_fixed(base_path, categorization):
    md_files = list(base_path.glob("*.md"))
    print(f"Found {len(md_files)} markdown files")
    
    file_data = []
    
    for file_path in md_files:
        filename = file_path.name
        # FIX: Convert filename to lowercase for dictionary lookup
        filename_lower = filename.lower()
        
        if filename_lower in categorization:
            category, subcategory = categorization[filename_lower]
            source = "Mapping"
        else:
            category, subcategory = auto_categorize(filename)
            source = "Auto"
        
        file_data.append({
            "filename": filename,
            "current_path": str(file_path),
            "category": category,
            "subcategory": subcategory
        })
    
    return pd.DataFrame(file_data)

# ==========================================
# 4. EXECUTION FUNCTION
# ==========================================
def execute_move(df_files, base_path):
    print(f"\nPreparing to move {len(df_files)} files...")
    
    # Create Backup Folder
    backup_dir = base_path / "00_Backup_Pre_Move"
    backup_dir.mkdir(exist_ok=True)
    
    moved_count = 0
    errors = []
    
    for _, row in df_files.iterrows():
        filename = row['filename']
        category = row['category']
        subcategory = row['subcategory']
        current_path = Path(row['current_path'])
        
        # Define destination
        if pd.isna(subcategory) or subcategory is None:
            dest_folder = base_path / category
        else:
            dest_folder = base_path / category / subcategory
            
        dest_path = dest_folder / filename
        
        # Skip if already there
        if current_path.parent == dest_folder:
            continue
            
        try:
            # 1. Create destination folder
            dest_folder.mkdir(parents=True, exist_ok=True)
            
            # 2. Create Backup
            shutil.copy2(current_path, backup_dir / filename)
            
            # 3. Move File
            shutil.move(str(current_path), str(dest_path))
            moved_count += 1
            
            if moved_count % 50 == 0:
                print(f"Moved {moved_count} files...")
                
        except Exception as e:
            errors.append(f"{filename}: {str(e)}")
            
    print(f"\nDONE! Successfully moved {moved_count} files.")
    if errors:
        print(f"Encountered {len(errors)} errors (check if Obsidian is open):")
        for err in errors[:5]:
            print(f" - {err}")

# ==========================================
# 5. RUN THE SCRIPT
# ==========================================

# 1. Analyze
print("Analyzing files...")
df_files = analyze_files_fixed(base_path, categorization)

# 2. Execute
# This input ensures you are ready
user_input = input(f"Ready to move {len(df_files)} files? (Type 'yes'): ")

if user_input.lower() == 'yes':
    execute_move(df_files, base_path)
else:
    print("Operation cancelled.")