import os
import pandas as pd
from pathlib import Path

def sanitize_filename(name):
    """Remove or replace invalid characters for Windows filenames"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '-')
    return name

def create_learning_path_structure():
    # Define the structure based on your table
    structure = [
        # Module 1
        {
            'module_num': '1',
            'module_name': 'Architect solutions for Dynamics 365 and Microsoft Power Platform',
            'chapters': [
                {
                    'chapter_num': '1.1',
                    'chapter_name': 'Becoming a solution architect for Dynamics 365 and Microsoft Power Platform',
                    'topics': [
                        {'topic_num': '1.1.1', 'topic_name': 'Introduction to becoming a solution architect'},
                        {'topic_num': '1.1.2', 'topic_name': 'Existing product and platform skills'},
                        {'topic_num': '1.1.3', 'topic_name': 'Expectations of a solution architect'},
                        {'topic_num': '1.1.4', 'topic_name': 'Solution architect role during project phases'},
                        {'topic_num': '1.1.5', 'topic_name': 'Pillars of a great architecture'},
                        {'topic_num': '1.1.6', 'topic_name': 'Check your knowledge - Becoming a solution architect'},
                        {'topic_num': '1.1.7', 'topic_name': 'Summary - Becoming a solution architect'}
                    ]
                },
                {
                    'chapter_num': '1.2',
                    'chapter_name': 'Discover customer needs as a Solution Architect for Dynamics 365 and Microsoft Power Platform',
                    'topics': [
                        {'topic_num': '1.2.1', 'topic_name': 'Introduction and discovery overview'},
                        {'topic_num': '1.2.2', 'topic_name': 'Initial customer discovery'},
                        {'topic_num': '1.2.3', 'topic_name': 'Customer discovery meetings'},
                        {'topic_num': '1.2.4', 'topic_name': 'Customer communication strategy'},
                        {'topic_num': '1.2.5', 'topic_name': 'Check your knowledge - Discover customer needs'},
                        {'topic_num': '1.2.6', 'topic_name': 'Summary - Discover customer needs'}
                    ]
                },
                {
                    'chapter_num': '1.3',
                    'chapter_name': 'Propose a solution as a Solution Architect for Microsoft Power Platform and Dynamics 365',
                    'topics': [
                        {'topic_num': '1.3.1', 'topic_name': 'Introduction and overview to proposing a solution'},
                        {'topic_num': '1.3.2', 'topic_name': 'Identify solution components'},
                        {'topic_num': '1.3.3', 'topic_name': 'Develop and validate a demo'},
                        {'topic_num': '1.3.4', 'topic_name': 'Identify potential third-party components'},
                        {'topic_num': '1.3.5', 'topic_name': 'Recognize strengths and weaknesses in a solution'},
                        {'topic_num': '1.3.6', 'topic_name': 'Check your knowledge - Propose a solution'},
                        {'topic_num': '1.3.7', 'topic_name': 'Summary - Propose a solution'}
                    ]
                },
                {
                    'chapter_num': '1.4',
                    'chapter_name': 'Work with requirements for Microsoft Power Platform and Dynamics 365',
                    'topics': [
                        {'topic_num': '1.4.1', 'topic_name': 'Introduction - Work with requirements'},
                        {'topic_num': '1.4.2', 'topic_name': 'Lead requirement capture sessions'},
                        {'topic_num': '1.4.3', 'topic_name': 'Identify functional requirements'},
                        {'topic_num': '1.4.4', 'topic_name': 'Identify non-functional requirements'},
                        {'topic_num': '1.4.5', 'topic_name': 'Confirm and finalize requirements'},
                        {'topic_num': '1.4.6', 'topic_name': 'Check your knowledge - Work with requirements'},
                        {'topic_num': '1.4.7', 'topic_name': 'Summary - Work with requirements'}
                    ]
                },
                {
                    'chapter_num': '1.5',
                    'chapter_name': 'Perform fit gap analysis',
                    'topics': [
                        {'topic_num': '1.5.1', 'topic_name': 'Introduction to fit gap analysis'},
                        {'topic_num': '1.5.2', 'topic_name': 'Determine feasibility of requirements'},
                        {'topic_num': '1.5.3', 'topic_name': 'Refine requirements from proof of concept insights'},
                        {'topic_num': '1.5.4', 'topic_name': 'Categorize business requirements and perform gap fit analysis'},
                        {'topic_num': '1.5.5', 'topic_name': 'Evaluate Dynamics 365 and Microsoft Power Platform apps'},
                        {'topic_num': '1.5.6', 'topic_name': 'Check your knowledge - Perform fit gap analysis'},
                        {'topic_num': '1.5.7', 'topic_name': 'Summary - Perform fit gap analysis'}
                    ]
                }
            ]
        },
        # Module 2 - Fixed: removed colon from folder names
        {
            'module_num': '2',
            'module_name': 'Solution Architect - Design Microsoft Power Platform solutions',
            'chapters': [
                {
                    'chapter_num': '2.1',
                    'chapter_name': 'Solution Architect series - Implement project governance for Power Platform and Dynamics 365',
                    'topics': [
                        {'topic_num': '2.1.1', 'topic_name': 'Introduction to project governance'},
                        {'topic_num': '2.1.2', 'topic_name': 'Project governance'},
                        {'topic_num': '2.1.3', 'topic_name': 'Solution architect\'s role in project governance'},
                        {'topic_num': '2.1.4', 'topic_name': 'Techniques for keeping a project on track'},
                        {'topic_num': '2.1.5', 'topic_name': 'Work as a team'},
                        {'topic_num': '2.1.6', 'topic_name': 'Check your knowledge - Implement project governance'},
                        {'topic_num': '2.1.7', 'topic_name': 'Summary - Implement project governance'}
                    ]
                },
                {
                    'chapter_num': '2.2',
                    'chapter_name': 'Solution Architect series - Power Platform architecture',
                    'topics': []  # No specific topics provided
                },
                {
                    'chapter_num': '2.3',
                    'chapter_name': 'Solution Architect series - Explore Power Apps architecture',
                    'topics': []  # No specific topics provided
                },
                {
                    'chapter_num': '2.4',
                    'chapter_name': 'Explore Power Automate architecture',
                    'topics': []  # No specific topics provided
                },
                {
                    'chapter_num': '2.5',
                    'chapter_name': 'Solution architect series - Explore Microsoft Copilot Studio',
                    'topics': []  # No specific topics provided
                },
                {
                    'chapter_num': '2.6',
                    'chapter_name': 'Solution architect series - Explore robotic process automation',
                    'topics': []  # No specific topics provided
                },
                {
                    'chapter_num': '2.7',
                    'chapter_name': 'Solution architect series - Model data for Power Platform solutions',
                    'topics': []  # No specific topics provided
                },
                {
                    'chapter_num': '2.8',
                    'chapter_name': 'Solution architect series - Model security for Power Platform solutions',
                    'topics': []  # No specific topics provided
                },
                {
                    'chapter_num': '2.9',
                    'chapter_name': 'Solution Architect series - Evaluate Power Platform analytics and AI',
                    'topics': []  # No specific topics provided
                },
                {
                    'chapter_num': '2.10',
                    'chapter_name': 'Solution Architect series - Implement integrations with Power Platform',
                    'topics': []  # No specific topics provided
                },
                {
                    'chapter_num': '2.11',
                    'chapter_name': 'Solution Architect series - Plan application lifecycle management for Power Platform',
                    'topics': []  # No specific topics provided
                },
                {
                    'chapter_num': '2.12',
                    'chapter_name': 'Solution Architect series - Testing and go-live',
                    'topics': []  # No specific topics provided
                }
            ]
        },
        # Module 3
        {
            'module_num': '3',
            'module_name': 'Validate your Microsoft Power Platform Solution Architect skills',
            'chapters': [
                {
                    'chapter_num': '3.1',
                    'chapter_name': 'Becoming a solution architect for Dynamics 365 and Microsoft Power Platform',
                    'topics': [
                        {'topic_num': '3.1.1', 'topic_name': 'Introduction to becoming a solution architect'},
                        {'topic_num': '3.1.2', 'topic_name': 'Existing product and platform skills'},
                        {'topic_num': '3.1.3', 'topic_name': 'Expectations of a solution architect'},
                        {'topic_num': '3.1.4', 'topic_name': 'Solution architect role during project phases'},
                        {'topic_num': '3.1.5', 'topic_name': 'Pillars of a great architecture'},
                        {'topic_num': '3.1.6', 'topic_name': 'Check your knowledge - Becoming a solution architect'},
                        {'topic_num': '3.1.7', 'topic_name': 'Summary - Becoming a solution architect'}
                    ]
                },
                {
                    'chapter_num': '3.2',
                    'chapter_name': 'Challenge project - Create Microsoft Power Platform solutions',
                    'topics': [
                        {'topic_num': '3.2.1', 'topic_name': 'Introduction - Challenge project'},
                        {'topic_num': '3.2.2', 'topic_name': 'Prepare - Challenge project'},
                        {'topic_num': '3.2.3', 'topic_name': 'Exercise - Create solutions for customers using Power Platform'},
                        {'topic_num': '3.2.4', 'topic_name': 'Module assessment - Challenge project'},
                        {'topic_num': '3.2.5', 'topic_name': 'Summary - Challenge project'}
                    ]
                }
            ]
        }
    ]
    
    return structure

def create_markdown_content(module_num, module_name, chapter_num, chapter_name, topic_num, topic_name):
    """Create the content for a markdown file"""
    content = f"""# {topic_num} - {topic_name}

## Module: {module_num} - {module_name}
## Chapter: {chapter_num} - {chapter_name}
## Topic: {topic_num} - {topic_name}

---

## Overview

This section covers: **{topic_name}**

## Key Concepts

- Placeholder for key concepts and learning objectives
- Add detailed content here
- Include examples and best practices

## Learning Objectives

By the end of this topic, you should be able to:
- Understand the core concepts of {topic_name}
- Apply the knowledge in practical scenarios
- Demonstrate proficiency in the subject matter

## Notes

Add your study notes and important points here.

---
*Part of the Microsoft Power Platform Solution Architect learning path*
"""
    return content

def create_folder_structure():
    """Create the complete folder and file structure"""
    structure = create_learning_path_structure()
    
    # Use a simpler base path to avoid long path issues
    base_path = Path("Power-Platform-Learning")
    
    for module in structure:
        # Create module folder with sanitized name
        module_folder_name = f"{module['module_num']} - {sanitize_filename(module['module_name'])}"
        module_path = base_path / module_folder_name
        module_path.mkdir(parents=True, exist_ok=True)
        
        print(f"Created module folder: {module_folder_name}")
        
        for chapter in module['chapters']:
            # Create chapter folder with sanitized name
            chapter_folder_name = f"{chapter['chapter_num']} - {sanitize_filename(chapter['chapter_name'])}"
            chapter_path = module_path / chapter_folder_name
            chapter_path.mkdir(parents=True, exist_ok=True)
            
            print(f"  Created chapter folder: {chapter_folder_name}")
            
            # Create topic markdown files
            if chapter['topics']:
                for topic in chapter['topics']:
                    # Create markdown file for each topic with sanitized name
                    filename = f"{topic['topic_num']} - {sanitize_filename(topic['topic_name'])}.md"
                    file_path = chapter_path / filename
                    
                    # Generate markdown content
                    content = create_markdown_content(
                        module['module_num'],
                        module['module_name'],  # Use original name for content
                        chapter['chapter_num'],
                        chapter['chapter_name'],  # Use original name for content
                        topic['topic_num'],
                        topic['topic_name']
                    )
                    
                    # Write the file
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"    Created file: {filename}")
                    except Exception as e:
                        print(f"    Error creating file {filename}: {str(e)}")
            else:
                # Create a placeholder file for chapters without specific topics
                placeholder_filename = f"{chapter['chapter_num']} - {sanitize_filename(chapter['chapter_name'])}.md"
                placeholder_path = chapter_path / placeholder_filename
                
                placeholder_content = f"""# {chapter['chapter_num']} - {chapter['chapter_name']}

## Module: {module['module_num']} - {module['module_name']}
## Chapter: {chapter['chapter_num']} - {chapter['chapter_name']}

---

## Overview

This chapter covers: **{chapter['chapter_name']}**

## Content Structure

- Detailed content to be added
- Learning materials and resources
- Practical exercises and examples

## Learning Path

Follow the structured learning path for comprehensive understanding.

---
*Part of the Microsoft Power Platform Solution Architect learning path*
"""
                
                try:
                    with open(placeholder_path, 'w', encoding='utf-8') as f:
                        f.write(placeholder_content)
                    print(f"    Created placeholder file: {placeholder_filename}")
                except Exception as e:
                    print(f"    Error creating placeholder file {placeholder_filename}: {str(e)}")

def main():
    print("Creating Power Platform Solution Architect Learning Path Structure...")
    print("=" * 70)
    
    try:
        create_folder_structure()
        print("\n" + "=" * 70)
        print("✅ Structure creation completed successfully!")
        print(f"📁 Root folder: Power-Platform-Learning")
        print("📚 Total modules: 3")
        print("📖 Multiple chapters and topics created")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print("\n💡 Tip: If you're still having issues, try running the script in a different directory with a shorter path.")

if __name__ == "__main__":
    main()
