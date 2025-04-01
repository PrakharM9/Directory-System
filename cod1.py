import os
import shutil
import streamlit as st
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

folder_path = "C:\Users\Amanjot Singh\Downloads\osproject files download"

def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                if not text.strip():
                    text = extract_text_with_orc(file_path)
                return text if text.strip()  else "No text xtracted"
        elif file_path.endswith(".docx"):
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text
         
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
    except Exception as e:
        st.error(f"⚠️ Error processing {file_path}: {e}")
        return ""
def extract_text_with_ocr(pdf_path) :
    try:
        images= convert_from_path(pdf_path)
        text = "\n".join([pytesseract.image_to_string(img)
        for img in images])
        return text if text.strip() else "No text detected"
    except Exception as e:
        print(f"OCR extraction failed for {pdf_path}: {e}")
        return "OCR extraction failed"

categories = {
    "Finance & Accounting": ["invoice", "budget", "tax", "bank", "salary", "account", "payroll", "statement", "financial", "transaction"],
    "Legal & Compliance": ["contract", "agreement", "law", "policy", "terms", "privacy", "compliance", "regulation", "dispute"],
    "Human Resources (HR)": ["resume", "employee", "recruitment", "onboarding", "training", "performance", "interview", "appraisal", "leave", "promotion"],
    "Project Management": ["task", "timeline", "deadline", "milestone", "strategy", "workflow", "roadmap", "progress", "sprint", "Gantt chart"],
    "Education & Research": ["thesis", "assignment", "lecture", "study", "research", "university", "paper", "experiment", "hypothesis", "citation"],
    "Marketing & Sales": ["campaign", "advertisement", "branding", "promotion", "lead", "customer", "sales", "SEO", "market", "analytics"],
    "IT & Software Development": ["code", "programming", "debug", "script", "repository", "framework", "database", "server", "API", "deployment"],
    "General Documents": ["report", "document", "memo", "summary", "meeting", "minutes", "presentation", "notes"],
    "Identity Documents": ["passport", "aadhaar", "license", "pan", "id card"],
    "Personal Documents": ["certificate", "marksheet", "migration", "transfer", "domicile", "identity", "aadhaar", "voter", "passport","driving license",
    "birth certificate","marriage certificate","degree","diploma"],
}

train_texts = [" ".join(keywords) for keywords in categories.values()]
train_labels = list(categories.keys())
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, train_labels)


def categorize_file(file_path):
    text_content = extract_text(file_path)
    print(f"Extracted text: {repr(text_content)}")
    if text_content is None:
        text_content = ""
    clean_text = text_content.strip()  
    return model.predict(vectorizer.transform([clean_text]))[0] if clean_text else "Uncategorized"


st.set_page_config(page_title="AI File Organizer", layout="centered", page_icon="📁")
st.title("📂 AI-Powered File Organizer")
st.write("This tool categorizes and organizes files into relevant folders.")

st.subheader("📋 Files Before Organization:")
files = os.listdir(folder_path)
st.write(", ".join(files) if files else "No files found.")
all_categories = list(categories.keys()) + ["Images", "Videos", "Uncategorized"]

if st.button("🔄 Restore Files"):
    moved_back_files = []
    for category in all_categories:
        category_path = os.path.join(folder_path, category)
        if os.path.exists(category_path):
            for file in os.listdir(category_path):
                shutil.move(os.path.join(category_path, file), os.path.join(folder_path, file))
                moved_back_files.append(f"🔄 {file} restored to main folder")
            shutil.rmtree(category_path)
    if moved_back_files:
        for restored_file in moved_back_files:
            st.success(restored_file)
    st.success("✅ Files have been restored to the main folder!")
if st.button("🗂️ Organize Files"):
    for category in all_categories:
        os.makedirs(os.path.join(folder_path, category), exist_ok=True)

    moved_files = []
    progress = st.progress(0)
    for index, file in enumerate(files):
        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path):
            file_ext = file.split('.')[-1].lower()
            if file_ext in ["jpg", "png", "jpeg"]:
                category = "Images"
            elif file_ext in ["mp4", "avi", "mkv"]:
                category = "Videos"
            elif file_ext in ["pdf", "docx", "txt"]:
                category = categorize_file(file_path)
            else:
                category = "Uncategorized"
            shutil.move(file_path, os.path.join(folder_path, category, file))
            moved_files.append(f"✅ {file} → {category}")
        progress.progress((index + 1) / len(files))
    if moved_files:
        st.subheader("📂 Organized Files:")
        for moved_file in moved_files:
            st.success(moved_file)
    else:
        st.warning("No files were moved. Everything might already be organized.")

    st.subheader("📁 Updated Folder Structure:")
    for category in all_categories:
        category_path = os.path.join(folder_path, category)
        if os.path.exists(category_path):
            category_files = os.listdir(category_path)
            if category_files:
                st.write(f"**📂 {category}:**")
                st.write(", ".join(category_files))

    st.success("✅ File organization complete!")

if st.button("🔄 Restore Files"):
    moved_back_files = []
    for category in all_categories:
        category_path = os.path.join(folder_path, category)
        if os.path.exists(category_path):
            for file in os.listdir(category_path):
                shutil.move(os.path.join(category_path, file), os.path.join(folder_path, file))
                moved_back_files.append(f"🔄 {file} restored to main folder")
            shutil.rmtree(category_path)
    if moved_back_files:
        for restored_file in moved_back_files:
            st.success(restored_file)
    st.success("✅ Files have been restored to the main folder!")

    