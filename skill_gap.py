import streamlit as st
import time

#Browser tab customization:
st.set_page_config(page_title="Skill-gap analyzer", layout="wide")

#Sidebar:
st.sidebar.title("Configuration")

analysis_depth = st.sidebar.select_slider(
    "In-depth analysis:",
    options=["Fast", "Standard", "Detailed"],
    value="Standard"
)

st.sidebar.write(f"Mode selected: {analysis_depth}")
st.sidebar.divider()
st.sidebar.markdown("### How to use")
st.sidebar.info("1. Upload your CV\n2. Paste the job description\n3. Click Analyze")

#Title:
st.title("Skill-gap analyzer")
st.markdown("Compare your professional profile against market requirements in real-time.")
st.divider()

#Body:
col1, col2 = st.columns(2)

col1.header("📂 Your profile")
uploaded_cv = col1.file_uploader("Upload your CV (PDF)", type="pdf")

col2.header("💼 Your target job")
job_title = col2.text_input("Job title:", placeholder="e.g., Senior Data Analyst")
job_desc = col2.text_area("Paste the job requirements here:", height=200)

st.divider()

c1, c2, c3 = st.columns([1, 1, 1])

if c2.button("🚀 Start match analysis", use_container_width=True):
    if (uploaded_cv) and job_desc:
        progress_bar = st.progress(0)
        st.info("Analyzing compatibility and identifying skill gaps...")
        
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        
        st.success("Analysis complete!")
       
        hard_skills = ["Python", "SQL", "Excel", "Tableau", "Power BI", "Statistics", "Machine Learning"]
        soft_skills = ["Leadership", "Communication", "Teamwork", "Agile", "Management"]
        languages = ["English", "Spanish", "French", "German"]

        cv_content = uploaded_cv.name if uploaded_cv else ""

        found_cv = [s for s in hard_skills + soft_skills + languages if s.lower() in cv_content.lower()]
        found_jd = [s for s in hard_skills + soft_skills + languages if s.lower() in job_desc.lower()]

        st.divider()
        st.header("📊 Evaluation results")

        m1, m2, m3 = st.columns(3)
        m1.metric("Overall Match", "72%", "+3% vs average")
        m2.metric("Skills Found", f"{len(found_cv)}")
        m3.metric("Skills to Improve", f"{len(found_jd) - len(found_cv) if len(found_jd) > len(found_cv) else 0}")

        st.subheader("Skill gap visualization")
        chart_data = {
            "Category": ["Hard Skills", "Soft Skills", "Languages"],
            "Your profile": [len([s for s in found_cv if s in hard_skills]), 
                             len([s for s in found_cv if s in soft_skills]), 
                             len([s for s in found_cv if s in languages])],
            "Your target job": [4, 3, 2]
        }
        st.bar_chart(data=chart_data, x="Category")

    else:
        st.error("Missing data: Please provide both your profile and the job description.")

    

