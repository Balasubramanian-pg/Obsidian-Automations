import os
import re
import yaml
from datetime import datetime
from pathlib import Path
import string

class MarkdownFrontMatterProcessor:
    def __init__(self):
        # Define topic categories and their keywords
        self.topic_keywords = {
            'Python Development': [
                'python', 'script', 'developer', 'code', 'programming', 'pandas', 
                'numpy', 'automation', 'api', 'flask', 'django'
            ],
            'Data Analysis': [
                'dataset', 'data', 'analysis', 'pbit', 'dax', 'power bi', 'tabular',
                'measure', 'analytics', 'metrics'
            ],
            'Productivity': [
                'productivity', 'tips', 'work', 'efficiency', 'optimize', 'resume',
                'summary', 'simplify', 'summarize'
            ],
            'Content Creation': [
                'tweet', 'thread', 'content', 'creator', 'canvas', 'obsidian',
                'ppt', 'presentation', 'email'
            ],
            'AI & Tools': [
                'chatgpt', 'gpt', 'ai', 'therapy', 'humanizer', 'fix', 'aestheticize'
            ]
        }
        
        # Define area categories
        self.area_categories = {
            'Technical': ['python', 'code', 'script', 'developer', 'dataset', 'pbit', 'dax'],
            'Professional': ['resume', 'work', 'productivity', 'ppt', 'presentation'],
            'Personal': ['therapy', 'summary', 'simplify', 'tweet', 'email'],
            'Tools': ['obsidian', 'chatgpt', 'ai', 'humanizer', 'tabular editor']
        }
        
        # Common tags mapping
        self.common_tags = {
            'python': ['programming', 'automation'],
            'data': ['analysis', 'powerbi', 'dax'],
            'productivity': ['efficiency', 'workflow'],
            'content': ['writing', 'social-media'],
            'ai': ['chatgpt', 'automation'],
            'summary': ['learning', 'knowledge'],
            'resume': ['career', 'professional'],
            'ppt': ['presentation', 'business']
        }

    def get_file_creation_date(self, file_path):
        """Get the file creation date from system properties"""
        try:
            if os.name == 'nt':
                creation_time = os.path.getctime(file_path)
            else:
                stat = os.stat(file_path)
                try:
                    creation_time = stat.st_birthtime
                except AttributeError:
                    creation_time = stat.st_mtime
            
            creation_date = datetime.fromtimestamp(creation_time)
            return creation_date.strftime('%Y-%m-%d')
            
        except Exception as e:
            print(f"Warning: Could not get creation date for {file_path.name}: {str(e)}")
            return datetime.now().strftime('%Y-%m-%d')

    def extract_keywords(self, text):
        """Extract meaningful keywords from text"""
        # Remove punctuation and convert to lowercase
        text = text.translate(str.maketrans('', '', string.punctuation)).lower()
        words = text.split()
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return meaningful_words

    def auto_assign_topic(self, filename, content):
        """Automatically assign topic based on filename and content analysis"""
        text_to_analyze = f"{filename} {content[:500] if content else ''}".lower()
        
        topic_scores = {}
        for topic, keywords in self.topic_keywords.items():
            score = sum(1 for keyword in keywords if keyword.lower() in text_to_analyze)
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            return max(topic_scores.items(), key=lambda x: x[1])[0]
        else:
            return "General"

    def auto_assign_area(self, filename, content):
        """Automatically assign area based on filename and content analysis"""
        text_to_analyze = f"{filename} {content[:500] if content else ''}".lower()
        
        area_scores = {}
        for area, keywords in self.area_categories.items():
            score = sum(1 for keyword in keywords if keyword.lower() in text_to_analyze)
            if score > 0:
                area_scores[area] = score
        
        if area_scores:
            return max(area_scores.items(), key=lambda x: x[1])[0]
        else:
            return "General"

    def auto_assign_tags(self, filename, content):
        """Automatically assign tags based on filename and content analysis"""
        text_to_analyze = f"{filename} {content[:200] if content else ''}".lower()
        keywords = self.extract_keywords(text_to_analyze)
        
        tags = set()
        
        # Add tags based on common mappings
        for word in keywords:
            if word in self.common_tags:
                tags.add(word)
                tags.update(self.common_tags[word])
        
        # Add specific tags based on content
        if any(word in text_to_analyze for word in ['python', 'script']):
            tags.update(['python', 'automation'])
        if any(word in text_to_analyze for word in ['data', 'dataset']):
            tags.update(['data', 'analysis'])
        if any(word in text_to_analyze for word in ['summary', 'summarize']):
            tags.update(['summary', 'learning'])
        if any(word in text_to_analyze for word in ['productivity', 'efficiency']):
            tags.update(['productivity', 'workflow'])
        if any(word in text_to_analyze for word in ['chatgpt', 'ai']):
            tags.update(['ai', 'automation'])
        
        # Ensure we have at least some tags
        if not tags:
            tags.update(['general', 'notes'])
        
        return sorted(list(tags))[:5]  # Return top 5 tags

    def parse_frontmatter(self, content):
        """Parse YAML front matter from markdown content"""
        front_matter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)'
        match = re.match(front_matter_pattern, content, re.DOTALL)
        
        if match:
            content_body = match.group(2)
            return {}, content_body  # Always return empty dict to remove existing properties
        else:
            return {}, content

    def create_standardized_frontmatter(self, file_path, content):
        """Create standardized front matter with auto-assigned properties"""
        filename = file_path.stem
        creation_date = self.get_file_creation_date(file_path)
        
        # Auto-assign properties
        topic = self.auto_assign_topic(filename, content)
        area = self.auto_assign_area(filename, content)
        tags = self.auto_assign_tags(filename, content)
        
        return {
            'Created Date': creation_date,
            'Area': area,
            'Tag': tags,
            'Topic': topic
        }

    def write_updated_content(self, file_path, front_matter, content_body):
        """Write updated content back to file"""
        front_matter_yaml = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True, sort_keys=False)
        updated_content = f"---\n{front_matter_yaml}---\n{content_body}"
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

    def process_markdown_files(self, folder_path, preview_only=False):
        """Process all markdown files in the folder"""
        folder = Path(folder_path)
        markdown_files = list(folder.glob("*.md"))
        
        if not markdown_files:
            print("No markdown files found in the specified folder.")
            return
        
        print(f"Found {len(markdown_files)} markdown files")
        print("\n" + "="*80)
        
        changes = []
        
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Parse content (always remove existing front matter)
                _, content_body = self.parse_frontmatter(content)
                
                # Create new standardized front matter
                new_front_matter = self.create_standardized_frontmatter(file_path, content_body)
                
                changes.append({
                    'file': file_path.name,
                    'new_properties': new_front_matter,
                    'content_preview': content_body[:100] + '...' if len(content_body) > 100 else content_body
                })
                
                if not preview_only:
                    self.write_updated_content(file_path, new_front_matter, content_body)
                
                print(f"\n📄 {file_path.name}")
                print(f"   Created Date: {new_front_matter['Created Date']}")
                print(f"   Area: {new_front_matter['Area']}")
                print(f"   Topic: {new_front_matter['Topic']}")
                print(f"   Tags: {', '.join(new_front_matter['Tag'])}")
                print(f"   Content Preview: {content_body[:80]}...")
                
            except Exception as e:
                print(f"✗ Error processing {file_path.name}: {str(e)}")
        
        return changes

def show_preview_changes(changes):
    """Show preview of changes before applying"""
    print("\n" + "="*80)
    print("PREVIEW OF CHANGES")
    print("="*80)
    
    for change in changes:
        print(f"\n📄 {change['file']}")
        print(f"   Created Date: {change['new_properties']['Created Date']}")
        print(f"   Area: {change['new_properties']['Area']}")
        print(f"   Topic: {change['new_properties']['Topic']}")
        print(f"   Tags: {', '.join(change['new_properties']['Tag'])}")

def main():
    processor = MarkdownFrontMatterProcessor()
    
    print("=== Markdown Front Matter Standardizer ===")
    print("This script will:")
    print("✅ Remove ALL existing front matter properties")
    print("✅ Add standardized properties: Created Date, Area, Tag, Topic")
    print("✅ Auto-assign Area, Tag, and Topic based on content analysis")
    print("✅ Use file system creation date for Created Date")
    
    # Use the specific folder path
    folder_path = r"C:\Users\ASUS\Videos\AnyDesk\Balasubramanian PG\01. Personal\Analyze\My Prompts"
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    
    print(f"\nTarget folder: {folder_path}")
    
    # First, show preview
    print("\n🔍 Analyzing files and generating preview...")
    changes = processor.process_markdown_files(folder_path, preview_only=True)
    
    if not changes:
        print("No changes to apply.")
        return
    
    # Show summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    area_counts = {}
    topic_counts = {}
    all_tags = []
    
    for change in changes:
        area = change['new_properties']['Area']
        topic = change['new_properties']['Topic']
        tags = change['new_properties']['Tag']
        
        area_counts[area] = area_counts.get(area, 0) + 1
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        all_tags.extend(tags)
    
    print("\nAreas distribution:")
    for area, count in sorted(area_counts.items()):
        print(f"  {area}: {count} files")
    
    print("\nTopics distribution:")
    for topic, count in sorted(topic_counts.items()):
        print(f"  {topic}: {count} files")
    
    print(f"\nTotal unique tags: {len(set(all_tags))}")
    
    # Confirm before applying
    confirm = input("\n🚀 Proceed with applying these changes? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Update cancelled.")
        return
    
    # Apply changes
    print("\n🔄 Applying changes...")
    processor.process_markdown_files(folder_path, preview_only=False)
    
    print("\n✅ All files have been successfully updated!")
    print("\nUpdated properties:")
    print("  • Created Date: From file system creation date")
    print("  • Area: Auto-assigned based on content (Technical/Professional/Personal/Tools)")
    print("  • Tag: Auto-generated relevant tags")
    print("  • Topic: Auto-categorized (Python Development/Data Analysis/Productivity/etc.)")

if __name__ == "__main__":
    main()
