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

            # Month folder: "08. August'25"
            month_num = date.strftime("%m")
            month_name = date.strftime("%B'%y")
            month_folder = f"{month_num}. {month_name}"

            # Final month folder path
            month_path = os.path.join(base, month_folder)
            os.makedirs(month_path, exist_ok=True)

            # Day folder: "01-08-25"
            day_folder_name = file.replace(".md", "")
            day_path = os.path.join(month_path, day_folder_name)
            os.makedirs(day_path, exist_ok=True)

            # Move the markdown file to the day folder
            shutil.move(file_path, os.path.join(day_path, file))

            print(f"Moved: {file} → {day_folder_name}/ inside {month_folder}")

        except ValueError:
            print("Skipped (not a date file):", file)
