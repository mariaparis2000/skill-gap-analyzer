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

        /* 2. RADIO BUTTONS (reemplazo del slider) - estilo custom */
        div[data-testid="stRadio"] div[role="radiogroup"] {
            display: flex !important;
            flex-direction: row !important;
            gap: 6px !important;
        }
        div[data-testid="stRadio"] label {
            background-color: #faf8f5 !important;
            border: 1px solid #e8ddd0 !important;
            border-radius: 10px !important;
            padding: 6px 14px !important;
            cursor: pointer !important;
        }
        div[data-testid="stRadio"] label:hover {
            border-color: #c9723a !important;
            background-color: #fdf3e7 !important;
        }

        /* 3. PROGRESS BAR - tono cálido apagado */
        div[data-testid="stProgressBar"] > div {
            background-color: #e8ddd0 !important;
        }
        div[data-testid="stProgressBar"] > div > div {
            background-color: #c9723a !important;
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
            border-left-color: #c9723a !important;
            color: #2d2d2d !important;
        }
        div[data-testid="stAlert"][kind="info"] p,
        div[data-testid="stAlert"][kind="info"] svg {
            color: #2d2d2d !important;
            fill: #c9723a !important;
        }

        /* 6. TEXT AREA & TEXT INPUT - fondo cálido, borde sutil */
        textarea, input[type="text"] {
            background-color: #fdf3e7 !important;
            border: 1px solid #e8ddd0 !important;
            border-radius: 10px !important;
            color: #2d2d2d !important;
        }
        textarea:focus, input[type="text"]:focus {
            border-color: #c9723a !important;
            box-shadow: 0 0 0 2px rgba(201, 114, 58, 0.2) !important;
        }

        /* 7. FILE UPLOADER - quitar azul, poner tono cálido */
        [data-testid="stFileUploader"] section {
            background-color: #fdf3e7 !important;
            border: 2px dashed #e8ddd0 !important;
            border-radius: 10px !important;
        }
        [data-testid="stFileUploader"] section:hover {
            border-color: #c9723a !important;
        }
        [data-testid="stFileUploader"] section svg {
            fill: #c9723a !important;
            color: #c9723a !important;
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
            border: 1px solid #c9723a !important;
            color: #c9723a !important;
            border-radius: 8px !important;
        }
        [data-testid="stFileUploader"] button:hover {
            background-color: #c9723a !important;
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
analysis_depth = st.sidebar.radio(
    "In-depth analysis:",
    options=["Fast", "Standard", "Detailed"],
    index=1,
    horizontal=True
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

        # Calcular porcentajes por categoría:
        def match_pct(cv_list, jd_list):
            if not jd_list:
                return 100
            matched = len([s for s in jd_list if s in cv_list])
            return round((matched / len(jd_list)) * 100)

        pct_hard = match_pct([s for s in found_cv if s in hard_skills], [s for s in found_jd if s in hard_skills])
        pct_soft = match_pct([s for s in found_cv if s in soft_skills], [s for s in found_jd if s in soft_skills])
        pct_lang = match_pct([s for s in found_cv if s in languages],   [s for s in found_jd if s in languages])
        pct_total = match_pct(found_cv, found_jd)

        def color_for(pct):
            if pct >= 75: return "#2e4d3d"
            if pct >= 40: return "#c9723a"
            return "#c0392b"

        # Gráfico total destacado + 3 categorías:
        def donut_html(pct, label, size=160):
            r = 54
            circ = 2 * 3.14159 * r
            fill = round((pct / 100) * circ, 1)
            gap  = round(circ - fill, 1)
            col  = color_for(pct)
            offset = round(circ / 4, 1)
            return f"""<div style="display:flex;flex-direction:column;align-items:center;gap:8px;">
                <svg width="{size}" height="{size}" viewBox="0 0 120 120">
                    <circle cx="60" cy="60" r="{r}" fill="none" stroke="#e8ddd0" stroke-width="10"/>
                    <circle cx="60" cy="60" r="{r}" fill="none" stroke="{col}" stroke-width="10"
                        stroke-dasharray="{fill} {gap}"
                        stroke-dashoffset="{offset}"
                        stroke-linecap="round"/>
                    <text x="60" y="55" text-anchor="middle" font-size="22" font-weight="bold" fill="#2d2d2d">{pct}%</text>
                    <text x="60" y="73" text-anchor="middle" font-size="9" fill="#6d6d6d">match</text>
                </svg>
                <span style="font-size:14px;font-weight:600;color:#2d2d2d;">{label}</span>
            </div>"""

        circ_total = 2 * 3.14159 * 54
        fill_total = round((pct_total / 100) * circ_total, 1)
        gap_total  = round(circ_total - fill_total, 1)
        offset_total = round(circ_total / 4, 1)
        col_total  = color_for(pct_total)

        overall_html = f"""<div style="display:flex;flex-direction:column;align-items:center;gap:8px;">
            <svg width="200" height="200" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="54" fill="none" stroke="#e8ddd0" stroke-width="11"/>
                <circle cx="60" cy="60" r="54" fill="none" stroke="{col_total}" stroke-width="11"
                    stroke-dasharray="{fill_total} {gap_total}"
                    stroke-dashoffset="{offset_total}"
                    stroke-linecap="round"/>
                <text x="60" y="53" text-anchor="middle" font-size="26" font-weight="bold" fill="#2d2d2d">{pct_total}%</text>
                <text x="60" y="71" text-anchor="middle" font-size="8.5" fill="#6d6d6d">overall match</text>
            </svg>
            <span style="font-size:16px;font-weight:700;color:#2d2d2d;">Overall Match</span>
        </div>"""

        hard_html = donut_html(pct_hard, "Hard Skills")
        soft_html = donut_html(pct_soft, "Soft Skills")
        lang_html = donut_html(pct_lang, "Languages")

        st.markdown(f"""
        <div style="background:#faf8f5;border-radius:24px;padding:32px 24px;border:1px solid #ffffff;margin-bottom:24px;">
            <div style="display:flex;justify-content:space-around;align-items:center;flex-wrap:wrap;gap:24px;">
                {overall_html}
                <div style="width:1px;height:140px;background:#e8ddd0;"></div>
                {hard_html}
                {soft_html}
                {lang_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Checklist:
        st.divider()
        st.subheader("✅ Skills Checklist")
        check_col1, check_col2 = st.columns(2)

        with check_col1:
            st.markdown("**Skills Found in your Profile:**")
            if found_cv:
                for skill in found_cv:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:5px 0;">
                        <span style="color:#2e4d3d;font-size:18px;">✅</span>
                        <span style="font-weight:600;color:#1a1a1a;">{skill}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("No matching skills found.")

        with check_col2:
            st.markdown("**Skills Missing (Required by Job):**")
            if missing_skills:
                for skill in missing_skills:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:5px 0;">
                        <span style="color:#c9723a;font-size:18px;">⬜</span>
                        <span style="font-weight:600;color:#1a1a1a;">{skill}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background-color:#2e4d3d;color:white;padding:10px;border-radius:10px;text-align:center;font-weight:bold;">
                    🌟 Analysis Complete! You have all the required skills.
                    </div>
                """, unsafe_allow_html=True)
        
    else:
        st.error("Missing data: Please provide both your profile (PDF or Text) and the job description.")