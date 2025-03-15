import os
import shutil
import streamlit as st
import pdfplumber
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

folder_path = "C:/Users/PRAKHAR MEHROTRA/Documents"

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
categories = {
    "Finance & Accounting": ["invoice", "budget", "tax", "bank", "salary", "account", "payroll", "statement", "financial", "transaction"],
    "Legal & Compliance": ["contract", "agreement", "law", "policy", "terms", "privacy", "compliance", "regulation", "dispute"],
    "Human Resources (HR)": ["resume", "employee", "recruitment", "onboarding", "training", "performance", "interview", "appraisal", "leave", "promotion"],
    "Project Management": ["task", "timeline", "deadline", "milestone", "strategy", "workflow", "roadmap", "progress", "sprint", "Gantt chart"],
    "Education & Research": ["thesis", "assignment", "lecture", "study", "research", "university", "paper", "experiment", "hypothesis", "citation"],
    "Marketing & Sales": ["campaign", "advertisement", "branding", "promotion", "lead", "customer", "sales", "SEO", "market", "analytics"],
    "IT & Software Development": ["code", "programming", "debug", "script", "repository", "framework", "database", "server", "API", "deployment"],
    "General Documents": ["report", "document", "memo", "summary", "meeting", "minutes", "presentation", "notes"],
}

train_texts = [" ".join(keywords) for keywords in categories.values()]
train_labels = list(categories.keys())
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)
model = KNeighborsClassifier(n_neighbors=1)
model.fit(X_train, train_labels)


def categorize_file(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        text = extract_text_from_txt(file_path)
    else:
        return "Uncategorized"

    if text.strip():
        X_test = vectorizer.transform([text])
        return model.predict(X_test)[0]
    
    return "Uncategorized"


st.title("📁 AI-Powered File Organizer")
st.write("Click the button below to organize files.")

if st.button("🗂️ Organize Files"):
    files = os.listdir(folder_path)

    file_categories = {
        "Images": ["jpg", "png", "jpeg"],
        "Videos": ["mp4", "avi", "mkv"],
    }

    all_categories = list(categories.keys()) + ["Images", "Videos", "Uncategorized"]
    for category in all_categories:
        category_path = os.path.join(folder_path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

    for file in files:
        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path):
            file_ext = file.split('.')[-1].lower()

            if file_ext in ["jpg", "png", "jpeg"]:
                shutil.move(file_path, os.path.join(folder_path, "Images", file))
                st.success(f"Moved {file} to Images")
            elif file_ext in ["mp4", "avi", "mkv"]:
                shutil.move(file_path, os.path.join(folder_path, "Videos", file))
                st.success(f"Moved {file} to Videos")
            
            elif file_ext in ["pdf", "docx", "txt"]:
                category = categorize_file(file_path)
                shutil.move(file_path, os.path.join(folder_path, category, file))
                st.success(f"Moved {file} to {category}")
            else:
                shutil.move(file_path, os.path.join(folder_path, "Uncategorized", file))
                st.warning(f"Moved {file} to Uncategorized")

    if "moved_files" in locals() and moved_files:
        st.write("### 📂 Moved Files:")
        for moved_file in moved_files:
            st.success(moved_file)
    else:
        st.warning("No files were moved. Maybe they are already organized?")

