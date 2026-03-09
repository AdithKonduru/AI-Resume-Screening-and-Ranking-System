import streamlit as st
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.resume_parser import extract_resume_text
from src.similarity_model import calculate_similarity
from src.skill_extractor import extract_skills

# Page configuration
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🤖",
    layout="wide"
)

# Header
st.markdown("""
# 🤖 AI Resume Screening System
### Automated Candidate Matching using NLP
""")

# Sidebar
st.sidebar.title("Project Info")
st.sidebar.write("AI Resume Screening System")
st.sidebar.write("Technologies Used:")
st.sidebar.write("- NLP (SpaCy)")
st.sidebar.write("- TF-IDF Similarity")
st.sidebar.write("- Streamlit")
st.sidebar.write("- Python")

# Load dataset
jobs = pd.read_csv("dataset/job_descriptions_dataset.csv")

# Layout columns
col1, col2 = st.columns(2)

with col1:
    job_role = st.selectbox("Select Job Role", jobs['job_title'])

with col2:
    uploaded_files = st.file_uploader(
        "Upload Resume PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

# Get job description
job_description = jobs[jobs['job_title'] == job_role]['skills'].iloc[0]
job_skills = [skill.strip().lower() for skill in job_description.split(",")]

results = []

# Process resumes
if uploaded_files:

    with st.spinner("Analyzing Resume(s)..."):
        for uploaded_resume in uploaded_files:
            temp_path = f"temp_{uploaded_resume.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_resume.getbuffer())
            resume_text = extract_resume_text(temp_path)
            score = calculate_similarity(resume_text, job_description)
            results.append((uploaded_resume.name, score))

            # Extract skills
            skills = extract_skills(resume_text)
            skills = [s.lower() for s in skills]

            matched = list(set(skills).intersection(set(job_skills)))
            missing = list(set(job_skills) - set(skills))

            st.divider()

            st.subheader(f"📄 Resume: {uploaded_resume.name}")

            # Resume preview
            st.write("Uploaded File:", uploaded_resume.name)

            # Match Score
            st.subheader("Match Score")

            st.progress(int(score * 100))

            st.metric("Resume Match", f"{round(score*100,2)}%")

            # Recommendation
            if score > 0.75:
                st.success("✅ Recommended Candidate")
            else:
                st.warning("⚠️ Not a Strong Match")

            # Metrics
            col1, col2, col3 = st.columns(3)

            col1.metric("Total Skills Required", len(job_skills))
            col2.metric("Skills Matched", len(matched))
            col3.metric("Skills Missing", len(missing))

            # Extracted skills
            st.subheader("Extracted Resume Skills")
            st.write(skills)

            # Skill Match
            st.subheader("Skill Match Analysis")

            st.write("✅ Matched Skills:", matched)
            st.write("❌ Missing Skills:", missing)

            # Visualization
            labels = ["Matched Skills", "Missing Skills"]
            sizes = [len(matched), len(missing)]

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%')
            ax.set_title("Skill Match Distribution")

            st.pyplot(fig)

# Ranking table
if results:
    st.divider()
    st.header("🏆 Candidate Ranking")
    df = pd.DataFrame(results, columns=["Resume", "Score"])
    df["Score"] = df["Score"] * 100
    df = df.sort_values(by="Score", ascending=False)
    st.dataframe(df)