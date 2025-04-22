import os
import shutil
import base64
import streamlit as st
from categorization import categorize_file, all_categories
from text_extraction import extract_text

folder_path = "C:/Users/PRAKHAR MEHROTRA/Desktop/Testing data"

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
                    ext = file.split('.')[-1].lower()
                    if ext in ["jpg", "png", "jpeg"]:
                        category = "Images"
                    elif ext in ["mp4", "avi", "mkv"]:
                        category = "Videos"
                    elif ext in ["pdf", "docx", "txt", "xls", "xlsx"]:
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