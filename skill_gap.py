import streamlit as st
import time

#Browser tab customization:
st.set_page_config(page_title="Skill-gap analyzer", layout="wide")

#Background:
st.markdown("""
    <style>
        /* Global background with a noticeable professional gradient */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        }

        /* Styling input containers for better contrast against the gradient */
        .stTextInput, .stTextArea, .stFileUploader {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
        }

        /* Unified sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #e0e4e8 !important;
        }
    </style>
""", unsafe_allow_html=True)

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
st.markdown("""
    <div style="background-color: #e3f2fd; padding: 30px; border-radius: 15px; border-left: 8px solid #1565c0; margin-bottom: 25px;">
        <h1 style="color: #0d47a1; margin: 0; font-family: sans-serif;">🎯 Skill-Gap AI Analyzer</h1>
        <p style="color: #1e88e5; font-size: 18px; margin-top: 10px;">Empowering your career path through data-driven insights.</p>
    </div>
""", unsafe_allow_html=True)
st.divider()

#Body:
col1, col2 = st.columns(2)

col1.header("📂 Your profile")
uploaded_cv = col1.file_uploader("Upload your CV (PDF)", type="pdf")
cv_text = col1.text_area("Or paste your skills/experience here:", height=150)

col2.header("💼 Your target job")
job_title = col2.text_input("Job title:", placeholder="e.g., Senior Data Analyst")
job_desc = col2.text_area("Paste the job requirements here:", height=200)

st.divider()

c1, c2, c3 = st.columns([1, 1, 1])

if c2.button("🚀 Start match analysis", use_container_width=True):
    if (uploaded_cv or cv_text) and job_desc:
        progress_bar = st.progress(0)
        st.info("Analyzing compatibility and identifying skill gaps...")
        
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        
        st.success("Analysis complete!")
       
        hard_skills = ["Python", "SQL", "Excel", "Tableau", "Power BI", "Statistics", "Machine Learning"]
        soft_skills = ["Leadership", "Communication", "Teamwork", "Agile", "Management"]
        languages = ["English", "Spanish", "French", "German"]

        file_name = uploaded_cv.name if uploaded_cv else ""
        cv_content = cv_text + " " + file_name

        found_cv = [s for s in hard_skills + soft_skills + languages if s.lower() in cv_content.lower()]
        found_jd = [s for s in hard_skills + soft_skills + languages if s.lower() in job_desc.lower()]

        st.divider()
        st.header("📊 Detailed Skill Analysis")

        # --- NEW SECTION: SIDE-BY-SIDE CHECKLIST ---
        st.subheader("✅ Skills Checklist")
        col_check1, col_check2 = st.columns(2)

        with col_check1:
            st.markdown("**Skills Found in your Profile:**")
            for skill in found_cv:
                # Usamos disabled=True porque es informativo, no para que el usuario clique
                st.checkbox(skill, value=True, key=f"found_{skill}", disabled=True)

        with col_check2:
            st.markdown("**Skills Missing (Required by Job):**")
            missing_skills = [s for s in found_jd if s not in found_cv]
            if missing_skills:
                for skill in missing_skills:
                    st.checkbox(skill, value=False, key=f"missing_{skill}", disabled=True)
            else:
                st.success("You have all the required skills mentioned in the JD!")

        st.divider()
        st.subheader("📈 Proficiency Gap")
        
        chart_data = {
            "Category": ["Hard Skills", "Soft Skills", "Languages"],
            "Current Profile": [len([s for s in found_cv if s in hard_skills]), 
                                len([s for s in found_cv if s in soft_skills]), 
                                len([s for s in found_cv if s in languages])],
            "Job Requirements": [4, 3, 2] # Mock requirements for comparison
        }
        st.bar_chart(
            data=chart_data, 
            x="Category", 
            y=["Current Profile", "Job Requirements"], 
            color=["#2e7d32", "#1565c0"], 
            stack=False
        )
        
    else:
        st.error("Missing data: Please provide both your profile and the job description.")

    

