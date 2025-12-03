import os
import yaml
from datetime import datetime
from pathlib import Path

def add_yaml_to_markdown(vault_path):
    """
    Add YAML frontmatter to markdown files in the specified vault path.
    Properties added:
    - Due: Current date (today's date)
    - Area: Parent folder name of the markdown file
    - Sub Area: Left blank
    """
    
    # Define the vault path
    vault = Path(vault_path)
    
    if not vault.exists():
        print(f"Error: Vault path '{vault}' does not exist.")
        return
    
    # Get current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Counter for processed files
    processed_count = 0
    
    # Walk through all directories and files in the vault
    for root, dirs, files in os.walk(vault):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                
                # Get the parent folder name (Area)
                parent_folder = Path(root).name
                
                # Read the existing content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if file already has YAML frontmatter
                has_frontmatter = False
                new_content = ""
                
                if content.startswith('---'):
                    # Extract existing frontmatter
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        has_frontmatter = True
                        existing_frontmatter = parts[1].strip()
                        rest_content = parts[2] if len(parts) > 2 else ""
                        
                        # Parse existing YAML
                        try:
                            frontmatter_data = yaml.safe_load(existing_frontmatter) or {}
                        except:
                            frontmatter_data = {}
                        
                        # Update with new properties (only if they don't exist)
                        if 'Due' not in frontmatter_data:
                            frontmatter_data['Due'] = current_date
                        if 'Area' not in frontmatter_data:
                            frontmatter_data['Area'] = parent_folder
                        if 'Sub Area' not in frontmatter_data:
                            frontmatter_data['Sub Area'] = ""
                        
                        # Create new YAML frontmatter
                        new_yaml = yaml.dump(frontmatter_data, default_flow_style=False, sort_keys=False)
                        new_content = f"---\n{new_yaml}---\n{rest_content}"
                else:
                    # Create new YAML frontmatter
                    frontmatter_data = {
                        'Due': current_date,
                        'Area': parent_folder,
                        'Sub Area': ""
                    }
                    
                    new_yaml = yaml.dump(frontmatter_data, default_flow_style=False, sort_keys=False)
                    new_content = f"---\n{new_yaml}---\n{content}"
                
                # Write the updated content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                processed_count += 1
                print(f"Processed: {file_path}")
    
    print(f"\nTotal markdown files processed: {processed_count}")

if __name__ == "__main__":
    # Your vault path
    vault_path = r"C:\Users\BalasubramanianPG\Videos\Obsidian Vault\Daily Reflection\The Action Plan\Projects"
    
    # Optional: Uncomment to use a relative path instead
    # vault_path = "./Interview Prep"
    
    print(f"Processing vault: {vault_path}")
    print("=" * 60)
    
    # Run the script
    add_yaml_to_markdown(vault_path)
    
    print("\nDone! YAML frontmatter has been added to all markdown files.")