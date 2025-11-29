import os
import shutil
from datetime import datetime

base = r"C:\Users\ASUS\Videos\AnyDesk\Balasubramanian PG\01. Personal\Analyze\Daily Reflections"

for file in os.listdir(base):
    if file.endswith(".md"):
        file_path = os.path.join(base, file)

        try:
            # Parse DD-MM-YY format
            date = datetime.strptime(file.replace(".md", ""), "%d-%m-%y")

            # Format folder name: November'25 etc
            folder_name = date.strftime("%B'%y")

            target_folder = os.path.join(base, folder_name)
            os.makedirs(target_folder, exist_ok=True)

            shutil.move(file_path, os.path.join(target_folder, file))
            print("Moved:", file)

        except ValueError:
            print("Skipped (not a date file):", file)
