import os
import re
from collections import Counter, defaultdict
import shutil

# Main directory containing all subfolders (Easy, Medium, Hard, etc.)
base_folder = r"C:\Users\BalasubramanianPG\Videos\Obsidian Vault\3. Interview Prep\Stratascratch"

# Output directory for organized files
output_base = r"C:\Users\BalasubramanianPG\Videos\Obsidian Vault\3. Interview Prep\Stratascratch\Organized_By_Patterns"

# Define difficulty mapping based on subfolder names
difficulty_mapping = {
    'Easy': 1,
    'Medium': 2, 
    'Hard': 3,
    'Advanced': 4
}

# Define topic family to chapter mapping (consolidated)
family_to_chapter = {
    "Aggregation Methods": 2,
    "Aggregate Functions": 2,
    "Aggregations": 2,
    "Data Retrieval Basics": 1,
    "Column Manipulation": 1,
    "Combining": 4,
    "Filtering Data": 3,
    "Distinct Counts": 2,
    "Boolean Indexing": 3,
    "DataFrame Operations": 4,
    "Data Cleaning": 1,
    "Conditional Logic": 3,
    "Unknown Family": 5
}

# Define function-based subcategories within chapters
function_to_subcategory = {
    # Aggregation functions
    '"agg()"': "Aggregations",
    '"count()"': "Counting",
    '"avg()"': "Averages",
    '"sum()"': "Summations",
    
    # Filtering functions
    '"arrange()"': "Sorting",
    '"between()"': "Range Filtering",
    '"is.na()"': "NULL Handling",
    '"coalesce()"': "NULL Handling",
    
    # Column operations
    '"alias()"': "Column Aliasing",
    '"col()"': "Column Selection",
    '"as.integer()"': "Type Conversion",
    '"as.character()"': "Type Conversion",
    '"as.Date()"': "Date Conversion",
    '"astype()"': "Type Conversion",
    
    # Joins & Combining
    '"bind_rows()"': "Row Combining",
    '"anti_join()"': "Anti Join",
    
    # Logic & Conditions
    '"case when"': "Conditional Logic",
    '"and"': "Logical Operations",
    
    # String functions
    '"contains()"': "String Operations",
    '"apply()"': "Function Application",
    
    # Default for unknown functions
    "Unknown Function": "Miscellaneous"
}

# Collect all topic data across all subfolders
all_topic_data = []
folder_stats = defaultdict(int)

# Walk through all subfolders in the base directory
for root, dirs, files in os.walk(base_folder):
    # Skip the output directory if it exists
    if output_base in root:
        continue
        
    for filename in files:
        if filename.endswith('.md'):
            file_path = os.path.join(root, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Extract YAML front matter
                yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
                if yaml_match:
                    yaml_content = yaml_match.group(1)
                    
                    # Find topic_family and topic_function
                    family_match = re.search(r'^topic_family:\s*(.*)', yaml_content, re.MULTILINE)
                    function_match = re.search(r'^topic_function:\s*(.*)', yaml_content, re.MULTILINE)
                    
                    family = family_match.group(1).strip() if family_match else "Unknown Family"
                    function = function_match.group(1).strip() if function_match else "Unknown Function"
                    
                    # Determine difficulty based on parent folder
                    parent_folder = os.path.basename(root)
                    difficulty = difficulty_mapping.get(parent_folder, 0)
                    
                    topic_data = {
                        'filename': filename,
                        'family': family,
                        'function': function,
                        'source_path': file_path,
                        'difficulty': difficulty,
                        'source_folder': parent_folder
                    }
                    
                    all_topic_data.append(topic_data)
                    folder_stats[parent_folder] += 1

# Count occurrences
family_counter = Counter(item['family'] for item in all_topic_data)
function_counter = Counter(item['function'] for item in all_topic_data)

print("=== ANALYSIS RESULTS ===")
print(f"Total files processed: {len(all_topic_data)}")
print(f"Files by source folder: {dict(folder_stats)}")
print(f"Unique topic families: {len(family_counter)}")
print(f"Unique topic functions: {len(function_counter)}")

print("\nTopic Family Counts:")
print("-" * 30)
for family, count in family_counter.items():
    print(f"- {family}: {count}")

print("\nTopic Function Counts:")
print("-" * 30)
for func, count in function_counter.items():
    print(f"- {func}: {count}")

# Organize files into new structure
os.makedirs(output_base, exist_ok=True)

# Group files by chapter and subcategory
organized_files = defaultdict(lambda: defaultdict(list))

for item in all_topic_data:
    family = item['family']
    function = item['function']
    difficulty = item['difficulty']
    
    # Determine chapter from family
    chapter_num = family_to_chapter.get(family, 5)  # Default to chapter 5
    
    # Add difficulty level to chapter number
    final_chapter = chapter_num + (difficulty * 10)  # So Easy=1, Medium=2, etc.
    
    # Determine subcategory from function
    # Handle the quoted function values properly
    subcategory = function_to_subcategory.get(function, "Miscellaneous")
    
    organized_files[final_chapter][subcategory].append(item)

# Create directory structure and move files
for chapter_num in sorted(organized_files.keys()):
    chapter_folder = f"Chapter_{chapter_num:02d}"
    chapter_path = os.path.join(output_base, chapter_folder)
    os.makedirs(chapter_path, exist_ok=True)
    
    print(f"\nCreating Chapter {chapter_num}...")
    
    for subcategory, items in organized_files[chapter_num].items():
        subfolder_name = subcategory.replace(" ", "_").replace("/", "_")
        subfolder_path = os.path.join(chapter_path, subfolder_name)
        os.makedirs(subfolder_path, exist_ok=True)
        
        print(f"  → {subcategory} ({len(items)} files)")
        
        for item in items:
            src = item['source_path']
            dst = os.path.join(subfolder_path, item['filename'])
            
            # Copy file to new location (use shutil.move() to move instead of copy)
            try:
                shutil.copy2(src, dst)  # Change to shutil.move() if you want to move
                print(f"    ✅ {item['filename']}")
            except Exception as e:
                print(f"    ❌ Error with {item['filename']}: {e}")
        
        # Create a summary file for this subcategory
        summary_file = os.path.join(subfolder_path, f"README.md")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# {subcategory}\n\n")
            f.write(f"**Chapter**: {chapter_num}\n")
            f.write(f"**Files**: {len(items)}\n\n")
            f.write("## Learning Objective\n")
            f.write("- Master this pattern\n")
            f.write("- Solve 3 problems daily\n")
            f.write("- Review weekly\n\n")
            f.write("## Files in this category:\n")
            for item in items:
                f.write(f"- {item['filename']} (from {item['source_folder']})\n")

print(f"\n🎉 Organization Complete!")
print(f"Output directory: {output_base}")
print(f"Total chapters created: {len(organized_files)}")
print(f"Total files processed: {len(all_topic_data)}")

# Print summary of new structure
print(f"\n=== NEW STRUCTURE SUMMARY ===")
for chapter_num in sorted(organized_files.keys()):
    print(f"Chapter {chapter_num}:")
    for subcategory, items in organized_files[chapter_num].items():
        print(f"  - {subcategory}: {len(items)} files")