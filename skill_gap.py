import streamlit as st
import time

#Browser tab:
st.set_page_config(page_title="Skill-gap analyzer", layout="wide")

#Background:
st.markdown("""
    <style>
        /* 1. SLIDER LINE - All in Forest Green */
        /* This targets both the progress and the remaining track */
        div[data-baseweb="slider"] > div > div, 
        div[data-baseweb="slider"] > div > div > div:first-child {
            background-color: #2e4d3d !important;
        }

        /* 2. SLIDER HANDLE (The circle) - Forest Green */
        div[data-baseweb="slider"] > div > div > div > div {
            background-color: #2e4d3d !important;
        }

        /* 3. TEXT LABELS (Fast, Standard, Detailed) */
        /* Black text, no background, no underline */
        div[data-baseweb="slider"] + div > div {
            background-color: transparent !important; /* No background box */
            color: #000000 !important; /* Pure Black */
            text-decoration: none !important; /* No underline */
            font-weight: 500 !important;
        }

        /* 4. SIDEBAR HEADERS & INFO */
        [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
            color: #000000 !important;
        }

        /* 5. MAIN BUTTON - Keeping the Forest Green for consistency */
        .stButton>button {
            background-color: #2e4d3d !important;
            color: #ffffff !important;
            border-radius: 20px;
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
st.sidebar.divider()
st.sidebar.markdown("### How to use")
st.sidebar.info("1. Upload your CV\n2. Paste the job description\n3. Click Analyze")

#Header:
st.markdown("""
    <div class="main-header">
        <h1 style="color: #2d2d2d; font-size: 45px; margin-bottom: 0;">Skill-Gap Analyzer</h1>
        <p style="color: #6d6d6d; font-size: 18px;">Match your skills with your dream job.</p>
    </div>
""", unsafe_allow_html=True)

#Body:
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("### 📝 Your Profile")
        uploaded_cv = st.file_uploader("Upload CV (PDF)", type="pdf", key="cv_uploader")
        cv_text = st.text_area("Or paste skills/summary:", height=150, placeholder="E.g., Python, SQL, Project Management...", key="cv_text_area")

with col2:
    with st.container():
        st.markdown("### 💼 Target Job")
        job_title = st.text_input("Job Title", placeholder="e.g. Data Scientist")
        job_desc = st.text_area("Job Requirements:", height=150, placeholder="Paste the job description here...", key="jd_text_area")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Start Match Analysis", use_container_width=True):
    if (uploaded_cv or cv_text) and job_desc:
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.info("Analyzing compatibility and identifying skill gaps...")
        
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        
        status_text.success("Analysis complete!")
        
        hard_skills = ["Python", "SQL", "Excel", "Tableau", "Power BI", "Statistics", "Machine Learning", "R", "Git"]
        soft_skills = ["Leadership", "Communication", "Teamwork", "Agile", "Management", "Problem Solving"]
        languages = ["English", "Spanish", "French", "German", "Italian"]

        file_name = uploaded_cv.name if uploaded_cv else ""
        cv_content = (cv_text if cv_text else "") + " " + file_name

        found_cv = [s for s in hard_skills + soft_skills + languages if s.lower() in cv_content.lower()]
        found_jd = [s for s in hard_skills + soft_skills + languages if s.lower() in job_desc.lower()]
        missing_skills = [s for s in found_jd if s not in found_cv]

        st.divider()
        st.header("📊 Detailed Skill Analysis")

        # Checklist:
        st.subheader("✅ Skills Checklist")
        check_col1, check_col2 = st.columns(2)

        with check_col1:
            st.markdown("**Skills Found in your Profile:**")
            if found_cv:
                for skill in found_cv:
                    st.checkbox(skill, value=True, key=f"found_{skill}", disabled=True)
            else:
                st.warning("No matching skills found.")

        with check_col2:
            st.markdown("**Skills Missing (Required by Job):**")
            if missing_skills:
                for skill in missing_skills:
                    st.checkbox(skill, value=False, key=f"missing_{skill}", disabled=True)
            else:
                st.markdown(f"""
                    <div style="background-color: #39e393; color: white; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold;">
                    🌟 Analysis Complete! Discover your professional roadmap below.
                    </div>
                """, unsafe_allow_html=True)

        # Chart
        st.divider()
        st.subheader("📈 Proficiency Gap")
        
        chart_data = {
            "Category": ["Hard Skills", "Soft Skills", "Languages"],
            "Current Profile": [
                len([s for s in found_cv if s in hard_skills]), 
                len([s for s in found_cv if s in soft_skills]), 
                len([s for s in found_cv if s in languages])
            ],
            "Job Requirements": [
                len([s for s in found_jd if s in hard_skills]), 
                len([s for s in found_jd if s in soft_skills]), 
                len([s for s in found_jd if s in languages])
            ]
        }
        
        st.bar_chart(
            data=chart_data, 
            x="Category", 
            y=["Current Profile", "Job Requirements"], 
            color=["#e68a4d", "#2e4d3d"], 
            stack=False
        )
        
    else:
        st.error("Missing data: Please provide both your profile (PDF or Text) and the job description.")