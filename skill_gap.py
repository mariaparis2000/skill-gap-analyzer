import streamlit as st
import time

#Browser tab:
st.set_page_config(page_title="Skill-gap analyzer", layout="wide")

#Background:
st.markdown("""
    <style>
        /* 1. GLOBAL & CONTAINERS */
        .stApp {
            background-color: #f2ede4;
        }

        .main-header {
            background: linear-gradient(135deg, #fcebdb 0%, #f7d7be 100%);
            padding: 40px; border-radius: 40px; text-align: center; margin-bottom: 30px;
        }

        [data-testid="stVerticalBlock"] > div:has(div[data-testid="stVerticalBlock"]) {
            background-color: #faf8f5;
            padding: 25px; border-radius: 30px 30px 80px 30px;
            border: 1px solid #ffffff; margin-bottom: 20px;
        }

        /* 2. SLIDER CLEANUP (NO BACKGROUNDS, NO UNDERLINES, PURE BLACK TEXT) */
        div[data-baseweb="slider"] span, 
        div[data-baseweb="slider"] div,
        div[data-testid="stTickBarItem"],
        [data-testid="stTickBar"] div {
            background-color: transparent !important;
            background: none !important;
            color: #000000 !important;
            text-decoration: none !important;
            text-decoration-line: none !important;
            border: none !important;
            box-shadow: none !important;
            -webkit-text-fill-color: #000000 !important;
        }

        /* Quitar subrayado - múltiples selectores para asegurar */
        div[data-baseweb="slider"] span,
        div[data-baseweb="slider"] span *,
        div[data-baseweb="tooltip"] span,
        div[data-baseweb="tooltip"] div,
        [data-testid="stSlider"] span,
        [data-testid="stSlider"] div span {
            text-decoration: none !important;
            text-decoration-line: none !important;
            border-bottom: none !important;
            box-shadow: none !important;
            outline: none !important;
        }

        div[data-baseweb="slider"] [data-testid="stWidgetLabel"],
        div[data-baseweb="slider"] [data-testid="stWidgetLabel"] * {
            text-decoration: none !important;
            text-decoration-line: none !important;
            box-shadow: none !important;
            border-bottom: none !important;
        }

        /* 3. SLIDER LINE COLORS */
        /* Left part (Progress): NARANJA */
        div[data-baseweb="slider"] > div > div > div:first-child {
            background-color: #e68a4d !important;
        }
        /* Right part (Remaining): BLACK */
        div[data-baseweb="slider"] > div > div {
            background-color: #000000 !important;
        }
        /* Knob (Circle): NARANJA */
        div[data-baseweb="slider"] > div > div > div > div {
            background-color: #e68a4d !important;
            border: none !important;
        }

        /* 4. MAIN BUTTON & SIDEBAR */
        .stButton>button {
            background-color: #2e4d3d !important;
            color: white !important;
            border-radius: 20px; border: none; padding: 10px 25px;
            font-weight: bold; width: 100%;
        }

        [data-testid="stSidebar"] {
            background-color: #f2ede4 !important;
        }

        /* 5. INFO BOX (st.info) - quitar azul, poner tono cálido */
        div[data-testid="stAlert"][kind="info"],
        div[data-baseweb="notification"] {
            background-color: #fdf3e7 !important;
            border-left-color: #e68a4d !important;
            color: #2d2d2d !important;
        }
        div[data-testid="stAlert"][kind="info"] p,
        div[data-testid="stAlert"][kind="info"] svg {
            color: #2d2d2d !important;
            fill: #e68a4d !important;
        }

        /* 6. TEXT AREA & TEXT INPUT - fondo cálido, borde sutil */
        textarea, input[type="text"] {
            background-color: #fdf3e7 !important;
            border: 1px solid #e8ddd0 !important;
            border-radius: 10px !important;
            color: #2d2d2d !important;
        }
        textarea:focus, input[type="text"]:focus {
            border-color: #e68a4d !important;
            box-shadow: 0 0 0 2px rgba(230, 138, 77, 0.2) !important;
        }

        /* 7. FILE UPLOADER - quitar azul, poner tono cálido */
        [data-testid="stFileUploader"] section {
            background-color: #fdf3e7 !important;
            border: 2px dashed #e8ddd0 !important;
            border-radius: 10px !important;
        }
        [data-testid="stFileUploader"] section:hover {
            border-color: #e68a4d !important;
        }
        [data-testid="stFileUploader"] section svg {
            fill: #e68a4d !important;
            color: #e68a4d !important;
        }
        [data-testid="stFileUploader"] section p,
        [data-testid="stFileUploader"] section small,
        [data-testid="stFileUploader"] section span {
            color: #6d6d6d !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] {
            color: #6d6d6d !important;
        }
        /* Botón Browse files */
        [data-testid="stFileUploader"] button {
            background-color: #fdf3e7 !important;
            border: 1px solid #e68a4d !important;
            color: #e68a4d !important;
            border-radius: 8px !important;
        }
        [data-testid="stFileUploader"] button:hover {
            background-color: #e68a4d !important;
            color: white !important;
        }

        /* 8. CHECKLIST STYLING */        
        div[data-testid="stCheckbox"] span[role="checkbox"][aria-checked="true"] {
            background-color: #39e393 !important;
            border-color: #39e393 !important;
        }
        .stCheckbox div[data-testid="stWidgetLabel"] p {
            color: #1a1a1a !important;
            font-weight: 700 !important;
            opacity: 1 !important;
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
                    <div style="background-color: #2e4d3d; color: white; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold;">
                    🌟 Analysis Complete! You have all the required skills.
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