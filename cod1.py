import os
import shutil
import streamlit as st
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import base64

folder_path ="C:/Users/PRAKHAR MEHROTRA/Desktop/Testing data"

def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                if not text.strip():
                    text = extract_text_with_ocr(file_path)
                return text if text.strip()  else "No text extracted"
        elif file_path.endswith(".docx"):
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text
         
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        elif file_path.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file_path, sheet_name=None) 
                text = ""
                for sheet in df.values():
                    text += sheet.astype(str).to_string()
                return text
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
    "Finance & Accounting": [
        "invoice", "budget", "tax", "bank", "salary", "account", "payroll", "statement", "financial", "transaction",
        "receipt", "expense", "revenue", "audit", "balance", "ledger", "dividend", "asset", "liability", "depreciation",
        "forecast", "investment", "reconciliation", "voucher", "credit", "debit", "profit", "loss", "GST", "invoice number",
        "fiscal", "quarter", "equity", "cash flow", "amortization", "IFRS", "GAAP", "capital", "reimbursement", "finance"
    ],
    
    "Legal & Compliance": [
        "contract", "agreement", "law", "policy", "terms", "privacy", "compliance", "regulation", "dispute",
        "legal", "license", "copyright", "trademark", "patent", "liability", "clause", "defendant", "plaintiff",
        "litigation", "arbitration", "bylaw", "statute", "verdict", "testimony", "affidavit", "deposition", "injunction",
        "settlement", "waiver", "disclosure", "jurisdiction", "enforcement", "breach", "confidentiality", "NDA",
        "indemnity", "warranty", "amendment", "stipulation", "legal notice", "prosecution", "subpoena"
    ],
    
    "Human Resources (HR)": [
        "resume", "employee", "recruitment", "onboarding", "training", "performance", "interview", "appraisal", "leave", "promotion",
        "CV", "candidate", "staff", "personnel", "benefits", "compensation", "termination", "resignation", "probation", "attendance",
        "timesheet", "orientation", "payslip", "career", "development", "workforce", "HRIS", "vacancy", "retention", "diversity",
        "inclusion", "welfare", "talent", "labor", "background check", "reference", "biometric", "offboarding", "grievance",
        "pension", "maternity", "paternity", "sabbatical", "severance", "overtime", "HR policy"
    ],
    
    "Project Management": [
        "task", "timeline", "deadline", "milestone", "strategy", "workflow", "roadmap", "progress", "sprint", "Gantt chart",
        "deliverable", "scope", "stakeholder", "agile", "waterfall", "Kanban", "Scrum", "JIRA", "risk", "resource",
        "allocation", "dependency", "critical path", "KPI", "objective", "burndown", "backlog", "iteration", "velocity",
        "release", "retrospective", "standup", "planning", "tracker", "project plan", "schedule", "WBS", "dashboard",
        "milestone report", "baseline", "bottleneck", "blockers", "implementation", "requirement", "status report"
    ],
    
    "Education & Research": [
        "thesis", "assignment", "lecture", "study", "research", "university", "paper", "experiment", "hypothesis", "citation",
        "dissertation", "professor", "student", "syllabus", "curriculum", "course", "scholarship", "academic", "journal",
        "literature review", "bibliography", "methodology", "abstract", "plagiarism", "peer review", "data analysis",
        "conference", "seminar", "workshop", "college", "faculty", "classroom", "laboratory", "fellowship", "degree program",
        "research grant", "publication", "institution", "education", "teacher", "learning", "pedagogy", "graduation", "alumni"
    ],
    
    "Marketing & Sales": [
        "campaign", "advertisement", "branding", "promotion", "lead", "customer", "sales", "SEO", "market", "analytics",
        "CRM", "social media", "strategy", "content", "conversion", "target audience", "demographic", "buyer persona",
        "funnel", "ROI", "marketing plan", "engagement", "influencer", "copywriting", "email marketing", "PPC", "CTR",
        "impression", "traffic", "bounce rate", "competitor", "proposal", "pitch", "upsell", "cross-sell", "retention",
        "acquisition", "prospect", "quota", "commission", "newsletter", "brand guidelines", "digital marketing", "CTA"
    ],
    
    "IT & Software Development": [
        "code", "programming", "debug", "script", "repository", "framework", "database", "server", "API", "deployment",
        "software", "hardware", "network", "algorithm", "architecture", "frontend", "backend", "UI/UX", "testing", "QA",
        "security", "encryption", "backup", "cloud", "DevOps", "CI/CD", "version control", "Git", "binary", "source code",
        "compiler", "runtime", "protocol", "interface", "bug", "patch", "feature", "release", "sprint", "agile",
        "microservice", "container", "Docker", "Kubernetes", "authentication", "authorization", "IT infrastructure", "SSL"
    ],
    
    "General Documents": [
        "report", "document", "memo", "summary", "meeting", "minutes", "presentation", "notes",
        "newsletter", "bulletin", "guide", "manual", "handbook", "whitepaper", "proposal", "agenda",
        "brief", "review", "analysis", "survey", "questionnaire", "form", "template", "draft", "revision",
        "announcement", "bulletin", "communication", "letter", "correspondence", "file", "folder", "attachment",
        "official", "reference", "directory", "catalog", "brochure", "gazette", "notification", "circular"
    ],
    
    "Identity Documents": [
        "passport", "aadhaar", "license", "pan", "id card", "voter id", "social security", "birth certificate",
        "biometric", "photo id", "government id", "identity proof", "residence proof", "nationality proof",
        "citizenship", "visa", "immigration", "green card", "address proof", "identity verification",
        "REAL ID", "national ID", "official ID", "authentication", "identification", "credential", "permanent resident card",
        "registration", "legal identity", "digital identity", "UIDAI", "SSN", "identification number"
    ],
    
    "Personal Documents": [
        "certificate", "marksheet", "migration", "transfer", "domicile", "identity", "aadhaar", "voter", "passport", "driving license",
        "birth certificate", "marriage certificate", "degree", "diploma", "transcript", "medical record", "vaccination",
        "immunization", "health insurance", "property deed", "title deed", "will", "testament", "power of attorney",
        "insurance policy", "utility bill", "bank statement", "residential proof", "income proof", "inheritance",
        "adoption paper", "divorce decree", "citizenship", "naturalization", "clearance certificate", "character certificate",
        "death certificate", "NOC", "bonafide", "caste certificate", "community certificate", "disability certificate"
    ],
}
all_categories = list(categories.keys()) + ["Images", "Videos", "Uncategorized"]

train_texts = [" ".join(keywords) for keywords in categories.values()]
train_labels = list(categories.keys())
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, train_labels)


def categorize_file(file_path):
    filename = os.path.basename(file_path).lower()
    text_content = extract_text(file_path)

    if not text_content or text_content == "No text extracted":
        return "Uncategorized"

    transformed_text = vectorizer.transform([text_content])
    predicted_category = model.predict(transformed_text)[0]
    distances, _ = model.kneighbors(transformed_text, n_neighbors=3)
    avg_distance = distances.mean()

    if avg_distance > 1.5:
        return "Uncategorized"

    return predicted_category

st.set_page_config(page_title="AI File Organizer", layout="wide", page_icon="📁")
st.title("📂 AI-Powered File Organizer")
st.markdown("Organize your files into intelligent categories using AI 🧠")

def set_bg_image(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode("utf-8") 
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_image("D:/Academics/OS Project/bg 2.png")
all_categories = list(categories.keys()) + ["Images", "Videos", "Uncategorized"]

with st.expander("📋 View Files in Main Folder", expanded=True):
    files = os.listdir(folder_path)
    if files:
        st.write("**Files:**")
        for f in files:
            st.write(f"• {f}")
    else:
        st.warning("No files found in the folder.")

col1, col2 = st.columns(2)

with col1:
    if st.button("🗂️ Organize Files"):
        moved_files = []

        with st.status("Organizing files... Please wait.", expanded=True) as status:
            for category in all_categories:
                os.makedirs(os.path.join(folder_path, category), exist_ok=True)

            for index, file in enumerate(files):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    file_ext = file.split('.')[-1].lower()
                    if file_ext in ["jpg", "png", "jpeg"]:
                        category = "Images"
                    elif file_ext in ["mp4", "avi", "mkv"]:
                        category = "Videos"
                    elif file_ext in ["pdf", "docx", "txt", "xls", "xlsx"]:
                        category = categorize_file(file_path)
                    else:
                        category = "Uncategorized"
                    shutil.move(file_path, os.path.join(folder_path, category, file))
                    moved_files.append(f"✅ {file} → {category}")
                status.update(label=f"Processing file {index+1}/{len(files)}...", state="running")
            status.update(label="Organization complete!", state="complete")

        if moved_files:
            st.success("✅ Files Organized Successfully!")
            with st.expander("📂 Organized File List", expanded=False):
                for msg in moved_files:
                    st.write(msg)
        else:
            st.warning("No files moved. Everything might already be organized.")

        with st.expander("📁 Updated Folder View"):
            for category in all_categories:
                cat_path = os.path.join(folder_path, category)
                if os.path.exists(cat_path):
                    cat_files = os.listdir(cat_path)
                    if cat_files:
                        st.markdown(f"**📂 {category}:**")
                        st.write(", ".join(cat_files))
with col2:
    moved_back_files = []  
    if st.button("🔄 Restore All Files to Main Folder"):
        with st.status("Restoring files...", expanded=True) as status:
            for root, _, files in os.walk(folder_path, topdown=False):
                if root == folder_path:
                    continue
                for file in files:
                    src = os.path.join(root, file)
                    dest = os.path.join(folder_path, file)
                    if os.path.exists(dest):
                        base, ext = os.path.splitext(file)
                        dest = os.path.join(folder_path, f"{base}_copy{ext}")
                    shutil.move(src, dest)
                    moved_back_files.append(f"🔄 {file} restored")

            for root, dirs, _ in os.walk(folder_path, topdown=False):
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)

            status.update(label="Files restored!", state="complete")

        if moved_back_files:
            st.success("✅ All files restored!")
            with st.expander("🔄 Restored File List", expanded=False):
                for msg in moved_back_files:
                    st.write(msg)
        else:
            st.info("No files found to restore.")
