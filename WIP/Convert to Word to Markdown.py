import os

def find_word_documents(root_folder):
    word_files = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for file in filenames:
            if file.lower().endswith(('.doc', '.docx')):
                full_path = os.path.join(dirpath, file)
                word_files.append(full_path)
    return word_files


# Set your root folder path here
root_path = r"C:\Users\BalasubramanianPG\Downloads\OneDrive_2025-11-27\01 SQL Training Program"   # Change this

documents = find_word_documents(root_path)

# Print results
for doc in documents:
    print(doc)

# Optional: write results to a file
# with open("word_documents_list.txt", "w", encoding="utf-8") as f:
#     for doc in documents:
#         f.write(doc + "\n")
