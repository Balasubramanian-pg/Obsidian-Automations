import os
import re
import datetime

# --- CONFIGURATION ---
# The root folder where your Obsidian Vault files are located.
# NOTE: Replace this with your actual, correct path.
ROOT_FOLDER = r"C:\Users\BalasubramanianPG\Videos\Obsidian Vault\Pharma Domain"

# The desired date format (DD-MM-YY)
DATE_FORMAT = "%d-%m-%y"

# The properties you want to ensure are in the YAML front matter.
# The values are set to defaults (date, empty lists/string).
YAML_TEMPLATE = {
    "Created": "",  # Will be populated with file creation date
    "Area": "[]",  # List for linking to other files
    "Tags": "[]",  # List for classifications
    "Description": '""',  # Text description
    "Sub Area": "[]"  # List for other files
}
# ---------------------


def get_file_creation_date(filepath):
    """
    Retrieves the file's creation timestamp and formats it.
    """
    try:
        # On Windows, 'st_ctime' is often the creation time.
        # Use 'st_mtime' (modification time) as a robust fallback/alternative
        # if creation time isn't reliably available or desired.
        timestamp = os.path.getctime(filepath)
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        return dt_object.strftime(DATE_FORMAT)
    except Exception as e:
        print(f"Error getting date for {filepath}: {e}")
        return datetime.datetime.now().strftime(DATE_FORMAT) # Fallback to current date

def update_yaml_front_matter(filepath, creation_date):
    """
    Reads a markdown file, updates/inserts YAML front matter, and writes changes.
    """
    print(f"Processing file: {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Prepare the properties with the current creation date
        current_yaml = YAML_TEMPLATE.copy()
        current_yaml["Created"] = f'"{creation_date}"'

        # 2. Check for existing YAML front matter (--- ... ---) at the very start
        yaml_match = re.match(r'---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)

        if yaml_match:
            # --- UPDATE EXISTING YAML ---
            existing_yaml_block = yaml_match.group(1)
            new_yaml_lines = existing_yaml_block.split('\n')
            existing_keys = set()
            
            # Use regex to find and replace existing keys
            for key, default_value in current_yaml.items():
                pattern = r"^" + re.escape(key) + r":.*$"
                replacement = f"{key}: {default_value}"
                
                # Check if the key already exists
                if re.search(pattern, existing_yaml_block, re.MULTILINE):
                    # Replace the existing line
                    existing_yaml_block = re.sub(pattern, replacement, existing_yaml_block, 1, re.MULTILINE)
                    existing_keys.add(key)
                
            # Add missing keys to the end of the YAML block
            missing_keys = [
                f"{key}: {current_yaml[key]}" 
                for key in current_yaml if key not in existing_keys
            ]
            
            if missing_keys:
                 existing_yaml_block += "\n" + "\n".join(missing_keys)

            # Reconstruct the full content
            new_yaml_block = f"---\n{existing_yaml_block.strip()}\n---"
            
            # The rest of the content after the original YAML block
            new_content = re.sub(r'---\s*\n(.*?)\n---\s*\n', new_yaml_block + '\n', content, 1, re.DOTALL)
            
        else:
            # --- INSERT NEW YAML ---
            yaml_lines = [f"{key}: {current_yaml[key]}" for key in current_yaml]
            new_yaml_block = "---\n" + "\n".join(yaml_lines) + "\n---"
            
            # Prepend the new YAML block to the existing content
            new_content = new_yaml_block + "\n" + content.strip()
            
        # 3. Write the updated content back to the file (No backup, as requested)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content.strip() + "\n")
            
        print(f"Successfully updated YAML in: {os.path.basename(filepath)}")

    except Exception as e:
        print(f"FAILED to process {filepath}. Error: {e}")


def main():
    """
    Walks the directory and calls the update function for each markdown file.
    """
    print(f"Starting script to update Markdown YAML properties in: {ROOT_FOLDER}")
    
    if not os.path.exists(ROOT_FOLDER):
        print(f"Error: The configured folder does not exist: {ROOT_FOLDER}")
        return
        
    md_file_count = 0
    
    # os.walk generates the file names in a directory tree
    for root, _, files in os.walk(ROOT_FOLDER):
        for filename in files:
            if filename.lower().endswith('.md'):
                md_file_count += 1
                filepath = os.path.join(root, filename)
                
                # 1. Get the creation date in the specified format
                creation_date = get_file_creation_date(filepath)
                
                # 2. Update/Insert the YAML front matter
                update_yaml_front_matter(filepath, creation_date)

    print("\n--- Script Finished ---")
    print(f"Total markdown files processed: {md_file_count}")
    print("Please review your files in Obsidian.")


if __name__ == "__main__":
    main()