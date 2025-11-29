import os
import re
import shutil

def capitalize_each_word(text):
    """Capitalize the first letter of each word in the text"""
    return ' '.join(word.capitalize() for word in text.split())

def process_markdown_files(root_folder):
    """Process all markdown files in the folder and subfolders"""
    
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.md'):
                # Get the full path of the markdown file
                md_file_path = os.path.join(root, file)
                
                # Remove the .md extension to get the base name
                base_name = os.path.splitext(file)[0]
                
                # Extract the numbering part and the title part
                # Pattern to match "number. title" format
                match = re.match(r'^(\d+\.\s*)(.*)$', base_name)
                
                if match:
                    number_part = match.group(1)  # e.g., "01. " or "16. "
                    title_part = match.group(2)   # e.g., "Lakehouse" or "Use Tools To Optimize Power BI Performance"
                    
                    # Capitalize each word in the title part
                    capitalized_title = capitalize_each_word(title_part)
                    
                    # Create the new folder name
                    new_folder_name = number_part + capitalized_title
                    
                    # Create the full path for the new folder
                    new_folder_path = os.path.join(root, new_folder_name)
                    
                    # Create the folder if it doesn't exist
                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)
                        print(f"Created folder: {new_folder_name}")
                    
                    # Move the markdown file into the folder
                    new_md_path = os.path.join(new_folder_path, file)
                    shutil.move(md_file_path, new_md_path)
                    print(f"Moved: {file} -> {new_folder_name}/")
                    
                else:
                    # If the file doesn't follow the numbering pattern, just capitalize each word
                    new_folder_name = capitalize_each_word(base_name)
                    new_folder_path = os.path.join(root, new_folder_name)
                    
                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)
                        print(f"Created folder: {new_folder_name}")
                    
                    # Move the markdown file into the folder
                    new_md_path = os.path.join(new_folder_path, file)
                    shutil.move(md_file_path, new_md_path)
                    print(f"Moved: {file} -> {new_folder_name}/")
                
                print("-" * 50)

def main():
    # Specify the root folder path
    root_folder = r"C:\Users\ASUS\Videos\AnyDesk\Balasubramanian PG\05. Projects\Fabric Project"
    
    # Check if the folder exists
    if not os.path.exists(root_folder):
        print(f"Error: The folder '{root_folder}' does not exist.")
        return
    
    print(f"Processing markdown files in: {root_folder}")
    print("-" * 50)
    
    # Process all markdown files
    process_markdown_files(root_folder)
    
    print("-" * 50)
    print("Processing completed!")

if __name__ == "__main__":
    main()
