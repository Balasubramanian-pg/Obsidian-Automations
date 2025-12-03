import os
import re
import string
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================

# Input file containing the roadmap text
INPUT_FILE_PATH = r"C:\Users\BalasubramanianPG\Music\Snowflake\README.md"

# The root directory where folders will be created
# (It uses the parent directory of the input file)
ROOT_DIR = os.path.dirname(INPUT_FILE_PATH)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def clean_text(text):
    """
    1. Removes leading/trailing special markers (#, *, -).
    2. Removes invalid file system characters.
    3. Replaces underscores with spaces.
    4. Converts to Title Case (Capitalize Each Word).
    5. Strips whitespace.
    """
    # Remove markdown markers from the start
    text = re.sub(r'^[\#\*\-\d\.]+\s*', '', text)
    
    # Remove invalid characters for Windows/Linux filenames
    # Invalid: < > : " / \ | ? *
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    
    # Replace underscores with spaces
    text = text.replace('_', ' ')
    
    # Capitalize each word (Title Case)
    text = string.capwords(text)
    
    return text.strip()

def get_todays_date():
    return datetime.now().strftime("%Y-%m-%d")

def create_frontmatter(area, sub_area):
    """
    Generates the YAML frontmatter string.
    Area = Main Heading
    Sub Area = Sub Heading
    """
    date_str = get_todays_date()
    # Handle cases where area/sub_area might be None
    area_val = area if area else "General"
    sub_area_val = sub_area if sub_area else "General"
    
    content = (
        "---\n"
        f"Created Date: {date_str}\n"
        "Updated Date: \n"
        f"Area: {area_val}\n"
        f"Sub area: {sub_area_val}\n"
        "---\n\n"
    )
    return content

# ==========================================
# MAIN LOGIC
# ==========================================

def process_roadmap():
    if not os.path.exists(INPUT_FILE_PATH):
        print(f"Error: Input file not found at {INPUT_FILE_PATH}")
        return

    print(f"Reading from: {INPUT_FILE_PATH}")
    print(f"Creating structure in: {ROOT_DIR}")

    with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # State variables
    current_part_path = None     # Level 1 Path
    current_main_path = None     # Level 2 Path
    current_sub_path = None      # Level 3/4 Path (Dynamic)
    
    # Text trackers for YAML Metadata
    current_main_heading_text = None  # To fill 'Area'
    current_sub_heading_text = None   # To fill 'Sub area'
    
    # Depth tracker to decide between Option B (Folder+Readme) and standard .md
    # 1 = Part, 2 = Main Heading, 3 = Sub Heading, 4 = Sub Sub Heading
    current_depth_level = 0 

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # ----------------------------------------
        # LEVEL 1: PART (# Part ...)
        # ----------------------------------------
        if line.startswith("# "):
            folder_name = clean_text(line)
            current_part_path = os.path.join(ROOT_DIR, folder_name)
            
            # Create Directory
            os.makedirs(current_part_path, exist_ok=True)
            
            # Reset lower levels
            current_main_path = None
            current_sub_path = None
            current_main_heading_text = None
            current_sub_heading_text = None
            current_depth_level = 1
            
            print(f"[Part] {folder_name}")

        # ----------------------------------------
        # LEVEL 2: MAIN HEADING (## ...)
        # ----------------------------------------
        elif line.startswith("## ") and current_part_path:
            folder_name = clean_text(line)
            current_main_path = os.path.join(current_part_path, folder_name)
            
            # Create Directory
            os.makedirs(current_main_path, exist_ok=True)
            
            # Update State
            current_sub_path = None # Reset sub path
            current_main_heading_text = folder_name
            current_sub_heading_text = None # Reset sub area
            current_depth_level = 2
            
            print(f"  [Main] {folder_name}")

        # ----------------------------------------
        # LEVEL 3: SUB HEADING (### ...)
        # ----------------------------------------
        elif line.startswith("### ") and current_main_path:
            folder_name = clean_text(line)
            current_sub_path = os.path.join(current_main_path, folder_name)
            
            # Create Directory
            os.makedirs(current_sub_path, exist_ok=True)
            
            # Update State
            current_sub_heading_text = folder_name
            current_depth_level = 3
            
            print(f"    [Sub] {folder_name}")

        # ----------------------------------------
        # LEVEL 4: SUB SUB HEADING (#### ...)
        # ----------------------------------------
        elif line.startswith("#### ") and current_sub_path:
            # Note: For Sub-Sub, we update the current_sub_path to go deeper
            # But we keep the 'Sub area' text as the parent Level 3, or update it?
            # User request: "Sub area - This will be the sub heading". 
            # I will update Sub Area to be specific to this level.
            folder_name = clean_text(line)
            
            # We append to the existing sub_path to create depth
            # But if previous line was level 3, current_sub_path is set.
            # We need to ensure we don't break logic if we go 3 -> 4 -> 4.
            # For simplicity in this script, #### is treated as a folder inside the active Level 3 path.
            
            temp_path = os.path.join(current_sub_path, folder_name)
            os.makedirs(temp_path, exist_ok=True)
            
            # Set this as the active path for bullets
            current_sub_path = temp_path 
            current_sub_heading_text = folder_name
            current_depth_level = 4
            
            print(f"      [Sub-Sub] {folder_name}")

        # ----------------------------------------
        # BULLETS / TOPICS (*, -, 1.)
        # ----------------------------------------
        elif re.match(r'^[\*\-1]\.?\s', line):
            if not current_main_path:
                continue # Skip bullets if no main header established

            topic_name = clean_text(line)
            
            # Determine YAML Metadata
            yaml_area = current_main_heading_text
            yaml_sub_area = current_sub_heading_text

            # LOGIC SPLIT: SHALLOW vs DEEP
            
            # Case A: Shallow (We are only at Level 2 - Main Heading)
            # Create Folder -> README.md
            if current_depth_level == 2:
                # In shallow mode, the Topic Name effectively becomes the Sub Area Context
                if not yaml_sub_area:
                    yaml_sub_area = topic_name

                topic_folder = os.path.join(current_main_path, topic_name)
                os.makedirs(topic_folder, exist_ok=True)
                
                file_path = os.path.join(topic_folder, "README.md")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    frontmatter = create_frontmatter(yaml_area, yaml_sub_area)
                    f.write(frontmatter)
                    f.write(f"# {topic_name}\n\nContent for {topic_name} goes here.")

            # Case B: Deep (We are at Level 3 or 4)
            # Create .md File directly
            elif current_depth_level >= 3:
                # In deep mode, sub_area is the ### header.
                file_name = f"{topic_name}.md"
                # current_sub_path holds the deepest folder created (Level 3 or 4)
                file_path = os.path.join(current_sub_path, file_name)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    frontmatter = create_frontmatter(yaml_area, yaml_sub_area)
                    f.write(frontmatter)
                    f.write(f"# {topic_name}\n\nContent for {topic_name} goes here.")

    print("\nProcessing Complete! Check your folder.")

if __name__ == "__main__":
    process_roadmap()