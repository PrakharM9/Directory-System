import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from text_extraction import extract_text

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
    if distances.mean() > 1.5:
        return "Uncategorized"
    return predicted_category
