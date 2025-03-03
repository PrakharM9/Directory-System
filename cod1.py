import os

folder_path = "C:/Users/PRAKHAR MEHROTRA/Documents"

files = os.listdir(folder_path)

for file in files:
    print(f"File: {file}, Type: {file.split('.')[-1]}")
import shutil

file_categories = {
    "Images": ["jpg", "png", "jpeg"],
    "Documents": ["pdf", "docx", "txt", "xlsx"],
    "Videos": ["mp4", "avi", "mkv"],
}
for category in file_categories.keys():
    category_path = os.path.join(folder_path, category)
    if not os.path.exists(category_path):
        os.makedirs(category_path)

for file in files:
    file_ext = file.split('.')[-1]  
    for category, extensions in file_categories.items():
        if file_ext in extensions:
            shutil.move(os.path.join(folder_path, file), os.path.join(folder_path, category, file))
            print(f"Moved {file} to {category}")
import pdfplumber

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text
