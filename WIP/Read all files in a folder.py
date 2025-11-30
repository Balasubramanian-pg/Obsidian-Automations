from pathlib import Path

def read_all_markdown_files(folder_path):
    """
    Read and display all markdown files in the specified folder.
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist!")
        return
    
    # Get all markdown files
    md_files = list(folder.glob('*.md'))
    
    if not md_files:
        print("No markdown files found in the folder.")
        return
    
    print(f"Found {len(md_files)} markdown files.\n")
    print("=" * 80)
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n📄 FILE: {file_path.name}")
            print("-" * 80)
            print(content)
            print("=" * 80)
            
        except Exception as e:
            print(f"✗ Error reading {file_path.name}: {str(e)}")

# Run the script
if __name__ == "__main__":
    folder_path = r"C:\Users\BalasubramanianPG\Videos\Obsidian Vault\Pharma Domain\Glossary Files"
    read_all_markdown_files(folder_path)