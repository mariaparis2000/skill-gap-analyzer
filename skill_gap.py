import streamlit as st
import time
import json
import re
from google import genai

st.set_page_config(page_title="Skill-gap analyzer", layout="wide")
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ── Real course database (verified URLs) ──────────────────────────────────────
COURSE_DB = {
    "Python":             {"course": "Python Bootcamp: From Zero to Hero", "instructor": "Jose Portilla", "platform": "Udemy", "level": "Beginner", "duration": "22 hours", "url": "https://www.udemy.com/course/complete-python-bootcamp/"},
    "SQL":                {"course": "The Complete SQL Bootcamp", "instructor": "Jose Portilla", "platform": "Udemy", "level": "Beginner", "duration": "9 hours", "url": "https://www.udemy.com/course/the-complete-sql-bootcamp/"},
    "Tableau":            {"course": "Tableau 2024 A-Z: Hands-On Tableau Training", "instructor": "Kirill Eremenko", "platform": "Udemy", "level": "Beginner", "duration": "9 hours", "url": "https://www.udemy.com/course/tableau10/"},
    "Power BI":           {"course": "Microsoft Power BI Desktop for Business Intelligence", "instructor": "Maven Analytics", "platform": "Udemy", "level": "Intermediate", "duration": "17 hours", "url": "https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/"},
    "Statistics":         {"course": "Statistics with Python Specialization", "instructor": "University of Michigan", "platform": "Coursera", "level": "Intermediate", "duration": "3 months", "url": "https://www.coursera.org/specializations/statistics-with-python"},
    "Machine Learning":   {"course": "Machine Learning Specialization", "instructor": "Andrew Ng", "platform": "Coursera", "level": "Intermediate", "duration": "3 months", "url": "https://www.coursera.org/specializations/machine-learning-introduction"},
    "Data Visualization": {"course": "Data Visualization with Python", "instructor": "IBM", "platform": "Coursera", "level": "Beginner", "duration": "12 hours", "url": "https://www.coursera.org/learn/python-for-data-visualization"},
    "Snowflake":          {"course": "Snowflake — The Complete Masterclass", "instructor": "Nikolai Schuler", "platform": "Udemy", "level": "Intermediate", "duration": "10 hours", "url": "https://www.udemy.com/course/snowflake-masterclass/"},
    "REST":               {"course": "REST API Design, Development & Management", "instructor": "AgileDad", "platform": "Udemy", "level": "Intermediate", "duration": "9 hours", "url": "https://www.udemy.com/course/rest-api/"},
    "Forecasting":        {"course": "Forecasting Models with Python", "instructor": "Jose Portilla", "platform": "Udemy", "level": "Advanced", "duration": "7 hours", "url": "https://www.udemy.com/course/forecasting-models-with-python/"},
    "Regression":         {"course": "Regression Analysis in Python", "instructor": "365 Careers", "platform": "Udemy", "level": "Intermediate", "duration": "5 hours", "url": "https://www.udemy.com/course/regression-analysis-in-python/"},
    "Deep Learning":      {"course": "Deep Learning Specialization", "instructor": "Andrew Ng", "platform": "Coursera", "level": "Advanced", "duration": "5 months", "url": "https://www.coursera.org/specializations/deep-learning"},
    "NLP":                {"course": "Natural Language Processing Specialization", "instructor": "DeepLearning.AI", "platform": "Coursera", "level": "Advanced", "duration": "4 months", "url": "https://www.coursera.org/specializations/natural-language-processing"},
    "AWS":                {"course": "AWS Certified Cloud Practitioner", "instructor": "Stephane Maarek", "platform": "Udemy", "level": "Beginner", "duration": "14 hours", "url": "https://www.udemy.com/course/aws-certified-cloud-practitioner-new/"},
    "Docker":             {"course": "Docker & Kubernetes: The Practical Guide", "instructor": "Maximilian Schwarzmüller", "platform": "Udemy", "level": "Intermediate", "duration": "24 hours", "url": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/"},
    "Git":                {"course": "The Git & Github Bootcamp", "instructor": "Colt Steele", "platform": "Udemy", "level": "Beginner", "duration": "17 hours", "url": "https://www.udemy.com/course/git-and-github-bootcamp/"},
    "Excel":              {"course": "Microsoft Excel — From Beginner to Expert", "instructor": "Kyle Pew", "platform": "Udemy", "level": "Beginner", "duration": "18 hours", "url": "https://www.udemy.com/course/microsoft-excel-2013-from-beginner-to-advanced-and-beyond/"},
    "R":                  {"course": "R Programming A-Z", "instructor": "Kirill Eremenko", "platform": "Udemy", "level": "Beginner", "duration": "10.5 hours", "url": "https://www.udemy.com/course/r-programming/"},
    "Communication":      {"course": "Communication Foundations", "instructor": "LinkedIn Learning", "platform": "LinkedIn Learning", "level": "Beginner", "duration": "1.5 hours", "url": "https://www.linkedin.com/learning/communication-foundations-2018"},
    "Critical Thinking":  {"course": "Critical Thinking & Problem Solving", "instructor": "Rochester Institute of Technology", "platform": "edX", "level": "Beginner", "duration": "4 weeks", "url": "https://www.edx.org/learn/critical-thinking-skills/rochester-institute-of-technology-critical-thinking-problem-solving"},
    "Presentation":       {"course": "Presentation Skills: Speechwriting, Slides & Delivery", "instructor": "TJ Walker", "platform": "Udemy", "level": "Beginner", "duration": "4 hours", "url": "https://www.udemy.com/course/presentation-skills-speechwriting/"},
    "Leadership":         {"course": "Leadership and Emotional Intelligence", "instructor": "Indian School of Business", "platform": "Coursera", "level": "Intermediate", "duration": "4 weeks", "url": "https://www.coursera.org/learn/leadership-emotion"},
    "Agile":              {"course": "Agile Fundamentals: Including Scrum & Kanban", "instructor": "Leanpitch", "platform": "Udemy", "level": "Beginner", "duration": "6.5 hours", "url": "https://www.udemy.com/course/agile-fundamentals-scrum-kanban-scrumban/"},
    "Project Management": {"course": "Google Project Management Certificate", "instructor": "Google", "platform": "Coursera", "level": "Beginner", "duration": "6 months", "url": "https://www.coursera.org/professional-certificates/google-project-management"},
    "ETL":                {"course": "ETL and Data Pipelines with Shell, Airflow and Kafka", "instructor": "IBM", "platform": "Coursera", "level": "Intermediate", "duration": "4 weeks", "url": "https://www.coursera.org/learn/etl-and-data-pipelines-shell-airflow-kafka"},
    "A/B Testing":        {"course": "A/B Testing by Google", "instructor": "Google/Udacity", "platform": "Udemy", "level": "Intermediate", "duration": "8 weeks", "url": "https://www.udacity.com/course/ab-testing--ud257"},
    "Scrum":              {"course": "Scrum Master Certification Prep", "instructor": "Valentin Despa", "platform": "Udemy", "level": "Beginner", "duration": "5 hours", "url": "https://www.udemy.com/course/scrum-master-certification-preparation-mock-exam-questions-psm-i/"},
    "Pandas":             {"course": "Data Analysis with Pandas and Python", "instructor": "Boris Paskhaver", "platform": "Udemy", "level": "Intermediate", "duration": "19.5 hours", "url": "https://www.udemy.com/course/data-analysis-with-pandas/"},
    "TensorFlow":         {"course": "TensorFlow Developer Certificate Bootcamp", "instructor": "Daniel Bourke", "platform": "Udemy", "level": "Advanced", "duration": "63 hours", "url": "https://www.udemy.com/course/tensorflow-developer-certificate-machine-learning-zero-to-mastery/"},
}

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        .stApp { background-color: #f2ede4; }
        .main-header {
            background: linear-gradient(135deg, #fcebdb 0%, #f7d7be 100%);
            padding: 40px; border-radius: 40px; text-align: center; margin-bottom: 30px;
        }
        [data-testid="stVerticalBlock"] > div:has(div[data-testid="stVerticalBlock"]) {
            background-color: #faf8f5; padding: 25px;
            border-radius: 30px 30px 80px 30px; border: 1px solid #ffffff; margin-bottom: 20px;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] { display: flex !important; flex-direction: row !important; gap: 6px !important; }
        div[data-testid="stRadio"] label { background-color: #faf8f5 !important; border: 1px solid #e8ddd0 !important; border-radius: 10px !important; padding: 6px 14px !important; cursor: pointer !important; }
        div[data-testid="stRadio"] label:hover { border-color: #c9723a !important; background-color: #fdf3e7 !important; }
        div[data-testid="stProgressBar"] > div { background-color: #e8ddd0 !important; }
        div[data-testid="stProgressBar"] > div > div { background-color: #c9723a !important; }
        .stButton>button { background-color: #2e4d3d !important; color: white !important; border-radius: 20px; border: none; padding: 10px 25px; font-weight: bold; width: 100%; }
        [data-testid="stSidebar"] { background-color: #f2ede4 !important; }
        div[data-testid="stAlert"][kind="info"], div[data-baseweb="notification"] { background-color: #fdf3e7 !important; border-left-color: #c9723a !important; color: #2d2d2d !important; }
        div[data-testid="stAlert"][kind="info"] p, div[data-testid="stAlert"][kind="info"] svg { color: #2d2d2d !important; fill: #c9723a !important; }
        textarea, input[type="text"] { background-color: #fdf3e7 !important; border: 1px solid #e8ddd0 !important; border-radius: 10px !important; color: #2d2d2d !important; }
        textarea:focus, input[type="text"]:focus { border-color: #c9723a !important; box-shadow: 0 0 0 2px rgba(201,114,58,0.2) !important; }
        [data-testid="stFileUploader"] section { background-color: #fdf3e7 !important; border: 2px dashed #e8ddd0 !important; border-radius: 10px !important; }
        [data-testid="stFileUploader"] section:hover { border-color: #c9723a !important; }
        [data-testid="stFileUploader"] section svg { fill: #c9723a !important; }
        [data-testid="stFileUploader"] section p, [data-testid="stFileUploader"] section small, [data-testid="stFileUploader"] section span { color: #6d6d6d !important; }
        [data-testid="stFileUploaderDropzoneInstructions"] { color: #6d6d6d !important; }
        [data-testid="stFileUploader"] button { background-color: #fdf3e7 !important; border: 1px solid #c9723a !important; color: #c9723a !important; border-radius: 8px !important; }
        [data-testid="stFileUploader"] button:hover { background-color: #c9723a !important; color: white !important; }
        .ai-coach-box {
            background: linear-gradient(135deg, #faf8f5 0%, #fdf3e7 100%);
            border: 1px solid #e8ddd0; border-left: 4px solid #2e4d3d;
            border-radius: 16px; padding: 28px 32px; margin-top: 8px;
            color: #2d2d2d; font-size: 15px; line-height: 1.7;
        }
        .course-card { background: #faf8f5; border: 1px solid #e8ddd0; border-radius: 16px; padding: 18px 20px; margin-bottom: 12px; transition: border-color 0.2s; }
        .course-card:hover { border-color: #c9723a; }
        .course-tag { display: inline-block; background: #fdf3e7; border: 1px solid #e8ddd0; border-radius: 20px; padding: 2px 10px; font-size: 12px; color: #c9723a; font-weight: 600; margin-right: 6px; }

        /* CHAT POPUP — fixed bottom right */
        #chat-popup-wrapper { position: fixed; bottom: 24px; right: 24px; z-index: 9999; width: 360px; font-family: sans-serif; }
        #chat-toggle-btn {
            background: #2e4d3d; color: white; border: none; border-radius: 50px;
            padding: 14px 22px; font-size: 15px; font-weight: 700; cursor: pointer;
            width: 100%; text-align: left; box-shadow: 0 4px 20px rgba(0,0,0,0.22);
            display: flex; align-items: center; gap: 10px;
        }
        #chat-box {
            background: #faf8f5; border: 1px solid #e8ddd0;
            border-radius: 20px 20px 4px 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15); margin-bottom: 10px;
            overflow: hidden; display: none; flex-direction: column; height: 460px;
        }
        #chat-box.open { display: flex; }
        #chat-header {
            background: #2e4d3d; color: white; padding: 14px 18px;
            font-weight: 700; font-size: 15px;
            display: flex; justify-content: space-between; align-items: center;
        }
        #chat-close { cursor: pointer; font-size: 16px; background: none; border: none; color: white; padding: 0; }
        #chat-messages {
            padding: 14px; overflow-y: auto; flex: 1;
            display: flex; flex-direction: column; gap: 10px;
        }
        .msg-user { background: #2e4d3d; color: white; border-radius: 14px 14px 4px 14px; padding: 10px 14px; font-size: 13px; align-self: flex-end; max-width: 85%; line-height: 1.5; }
        .msg-bot { background: #fdf3e7; border: 1px solid #e8ddd0; border-radius: 14px 14px 14px 4px; padding: 10px 14px; font-size: 13px; align-self: flex-start; max-width: 85%; color: #2d2d2d; line-height: 1.5; }
        #chat-input-row { display: flex; gap: 8px; padding: 10px 14px; border-top: 1px solid #e8ddd0; background: #faf8f5; }
        #chat-input { flex: 1; border: 1px solid #e8ddd0; border-radius: 20px; padding: 8px 14px; font-size: 13px; background: #fdf3e7; outline: none; color: #2d2d2d; }
        #chat-input:focus { border-color: #c9723a; }
        #chat-send { background: #2e4d3d; color: white; border: none; border-radius: 20px; padding: 8px 16px; font-size: 14px; font-weight: 700; cursor: pointer; }
        #chat-send:hover { background: #3d6b52; }
    </style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.title("Configuration")
analysis_depth = st.sidebar.radio("In-depth analysis:", options=["Fast", "Standard", "Detailed"], index=1, horizontal=True)
st.sidebar.divider()
st.sidebar.markdown("### How to use")
st.sidebar.info("1. Upload your CV\n2. Paste the job description\n3. Click Analyze")

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="main-header">
        <h1 style="color:#2d2d2d;font-size:45px;margin-bottom:0;">Skill-Gap Analyzer</h1>
        <p style="color:#6d6d6d;font-size:18px;">Match your skills with your dream job.</p>
    </div>
""", unsafe_allow_html=True)

# ── Inputs ─────────────────────────────────────────────────────────────────────
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

# ── Handle chat message BEFORE the main button (so rerun doesn't re-trigger analysis) ──
params = st.query_params
if "chat_msg" in params and st.session_state.get("analysis_done"):
    user_input = params["chat_msg"]
    st.query_params.clear()

    if not st.session_state["chat_history"] or st.session_state["chat_history"][-1]["content"] != user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        system_context = f"""You are a friendly expert career coach. You already analyzed this candidate.
CV summary: {st.session_state.get('cv_content','')[:300]}
Target job: {st.session_state.get('job_title','')} — {st.session_state.get('job_desc','')[:300]}
Skills they have: {st.session_state.get('found_cv',[])}
Skills missing: {st.session_state.get('missing_skills',[])}
Be concise, encouraging, practical. Max 3 short paragraphs. Reply in English."""

        conversation = system_context + "\n\n"
        for msg in st.session_state["chat_history"]:
            role = "Candidate" if msg["role"] == "user" else "Coach"
            conversation += f"{role}: {msg['content']}\n"
        conversation += "Coach:"

        try:
            chat_response = client.models.generate_content(model="gemini-2.0-flash", contents=conversation)
            bot_reply = chat_response.text.strip()
        except Exception as e:
            bot_reply = "I'm having trouble connecting right now. Please try again!"

        st.session_state["chat_history"].append({"role": "assistant", "content": bot_reply})
        st.rerun()

# ── Analysis ───────────────────────────────────────────────────────────────────
if st.button("🚀 Start Match Analysis", use_container_width=True):
    if (uploaded_cv or cv_text) and job_desc:

        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.info("Analyzing compatibility and identifying skill gaps...")
        for i in range(60):
            time.sleep(0.01)
            progress_bar.progress(i + 1)

        pdf_text = ""
        if uploaded_cv:
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(uploaded_cv)
                for page in reader.pages:
                    pdf_text += page.extract_text() or ""
            except Exception as e:
                st.warning(f"Could not read PDF: {e}")

        pdf_text = re.sub(r'\s+', ' ', pdf_text)
        cv_content = (cv_text if cv_text else "") + " " + pdf_text

        aliases = {
            "Power BI": ["PowerBI", "powerbi"], "Machine Learning": ["machine learning", "ML"],
            "Data Visualization": ["data visualization", "data viz"],
            "Communication": ["communicating", "communications"],
            "Critical Thinking": ["critical thinking"], "Presentation": ["presentations", "presenting"],
            "Statistics": ["statistical", "stats"], "Python": ["python"], "SQL": ["sql"],
            "Tableau": ["tableau"], "AWS": ["aws"], "Excel": ["excel"],
            "Agile": ["agile"], "Leadership": ["leadership", "leading", "led"],
            "Teamwork": ["teamwork", "cross-functional"], "Project Management": ["project management"],
        }
        injections = []
        cv_lower = cv_content.lower()
        for canonical, variants in aliases.items():
            for v in variants:
                if v.lower() in cv_lower:
                    injections.append(canonical)
                    break
        cv_content = cv_content + " " + " ".join(injections)

        depth_instructions = {
            "Fast": "Be concise. Give a brief 2-3 sentence summary only.",
            "Standard": "Give a balanced analysis with key points and actionable advice.",
            "Detailed": "Give an in-depth analysis with specific examples, priorities, and a step-by-step action plan."
        }

        hard_skills = ["Python","SQL","Excel","Tableau","Power BI","Statistics","Machine Learning","R","Git","TensorFlow","PyTorch","Scikit-learn","Pandas","NumPy","Matplotlib","Deep Learning","NLP","Computer Vision","Data Visualization","Big Data","Spark","Hadoop","AWS","Azure","GCP","Docker","Kubernetes","Java","JavaScript","TypeScript","React","Node.js","HTML","CSS","MongoDB","PostgreSQL","MySQL","Airflow","dbt","Looker","Snowflake","Databricks","Kafka","API","REST","A/B Testing","Forecasting","Regression","Classification","Clustering","SPSS","SAS","Scala","ETL","Data Engineering","MLOps","CI/CD"]
        soft_skills = ["Leadership","Communication","Teamwork","Agile","Management","Problem Solving","Critical Thinking","Creativity","Collaboration","Adaptability","Time Management","Project Management","Scrum","Kanban","Stakeholder Management","Presentation","Negotiation","Mentoring","Strategic Thinking","Decision Making","Analytical Thinking","Attention to Detail","Customer Focus","Innovation","Conflict Resolution"]
        languages = ["English","Spanish","French","German","Italian","Portuguese","Chinese","Mandarin","Japanese","Arabic","Dutch","Russian","Korean","Swedish","Catalan"]

        found_cv_hard = [s for s in hard_skills if s.lower() in cv_content.lower()]
        found_cv_soft = [s for s in soft_skills if s.lower() in cv_content.lower()]
        found_cv_lang = [s for s in languages  if s.lower() in cv_content.lower()]
        found_jd_hard = [s for s in hard_skills if s.lower() in job_desc.lower()]
        found_jd_soft = [s for s in soft_skills if s.lower() in job_desc.lower()]
        found_jd_lang = [s for s in languages  if s.lower() in job_desc.lower()]

        found_cv = found_cv_hard + found_cv_soft + found_cv_lang
        found_jd = found_jd_hard + found_jd_soft + found_jd_lang
        missing_skills = [s for s in found_jd if s not in found_cv]
        missing_hard = [s for s in found_jd_hard if s not in found_cv_hard]
        missing_soft = [s for s in found_jd_soft if s not in found_cv_soft]
        missing_lang = [s for s in found_jd_lang if s not in found_cv_lang]

        # Save to session state — persists across reruns so chatbot works:
        st.session_state["analysis_done"] = True
        st.session_state["cv_content"] = cv_content
        st.session_state["job_desc"] = job_desc
        st.session_state["job_title"] = job_title
        st.session_state["found_cv"] = found_cv
        st.session_state["missing_skills"] = missing_skills
        st.session_state["chat_history"] = []  # reset chat on new analysis

        for i in range(60, 100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        status_text.success("Analysis complete!")

        st.divider()
        st.header("📊 Detailed Skill Analysis")

        def match_pct(cv_list, jd_list):
            if not jd_list: return 100
            return round(len([s for s in jd_list if s in cv_list]) / len(jd_list) * 100)

        pct_hard  = match_pct(found_cv_hard, found_jd_hard)
        pct_soft  = match_pct(found_cv_soft, found_jd_soft)
        pct_lang  = match_pct(found_cv_lang, found_jd_lang)
        pct_total = match_pct(found_cv, found_jd)
        st.session_state["pct_total"] = f"{pct_total}%"

        def color_for(pct):
            if pct >= 75: return "#2e4d3d"
            if pct >= 40: return "#c9723a"
            return "#c0392b"

        def donut_html(pct, label, size=160):
            r, circ = 54, 2 * 3.14159 * 54
            fill = round((pct / 100) * circ, 1)
            return f"""<div style="display:flex;flex-direction:column;align-items:center;gap:8px;">
                <svg width="{size}" height="{size}" viewBox="0 0 120 120">
                    <circle cx="60" cy="60" r="{r}" fill="none" stroke="#e8ddd0" stroke-width="10"/>
                    <circle cx="60" cy="60" r="{r}" fill="none" stroke="{color_for(pct)}" stroke-width="10"
                        stroke-dasharray="{fill} {round(circ-fill,1)}" stroke-dashoffset="{round(circ/4,1)}" stroke-linecap="round"/>
                    <text x="60" y="55" text-anchor="middle" font-size="22" font-weight="bold" fill="#2d2d2d">{pct}%</text>
                    <text x="60" y="73" text-anchor="middle" font-size="9" fill="#6d6d6d">match</text>
                </svg>
                <span style="font-size:14px;font-weight:600;color:#2d2d2d;">{label}</span>
            </div>"""

        circ = 2 * 3.14159 * 54
        fill_t = round((pct_total / 100) * circ, 1)
        overall_html = f"""<div style="display:flex;flex-direction:column;align-items:center;gap:8px;">
            <svg width="200" height="200" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="54" fill="none" stroke="#e8ddd0" stroke-width="11"/>
                <circle cx="60" cy="60" r="54" fill="none" stroke="{color_for(pct_total)}" stroke-width="11"
                    stroke-dasharray="{fill_t} {round(circ-fill_t,1)}" stroke-dashoffset="{round(circ/4,1)}" stroke-linecap="round"/>
                <text x="60" y="53" text-anchor="middle" font-size="26" font-weight="bold" fill="#2d2d2d">{pct_total}%</text>
                <text x="60" y="71" text-anchor="middle" font-size="8.5" fill="#6d6d6d">overall match</text>
            </svg>
            <span style="font-size:16px;font-weight:700;color:#2d2d2d;">Overall Match</span>
        </div>"""

        st.markdown(f"""
        <div style="background:#faf8f5;border-radius:24px;padding:32px 24px;border:1px solid #ffffff;margin-bottom:24px;">
            <div style="display:flex;justify-content:space-around;align-items:center;flex-wrap:wrap;gap:24px;">
                {overall_html}
                <div style="width:1px;height:140px;background:#e8ddd0;"></div>
                {donut_html(pct_hard,"Hard Skills")} {donut_html(pct_soft,"Soft Skills")} {donut_html(pct_lang,"Languages")}
            </div>
        </div>""", unsafe_allow_html=True)

        st.divider()
        st.subheader("✅ Skills Checklist")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Skills Found in your Profile:**")
            for s in found_cv:
                st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:5px 0;"><span style="font-size:18px;">✅</span><span style="font-weight:600;color:#1a1a1a;">{s}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown("**Skills Missing (Required by Job):**")
            if missing_skills:
                for s in missing_skills:
                    st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:5px 0;"><span style="font-size:18px;">❌</span><span style="font-weight:600;color:#1a1a1a;">{s}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="background:#2e4d3d;color:white;padding:10px;border-radius:10px;text-align:center;font-weight:bold;">🌟 You have all the required skills!</div>', unsafe_allow_html=True)

        st.divider()
        st.subheader("🤖 AI Career Coach")
        with st.spinner("Generating personalized career advice..."):
            coach_prompt = f"""Career coach. Skill gap analysis:
Match: {pct_total}% overall, {pct_hard}% hard, {pct_soft}% soft, {pct_lang}% languages.
Strong skills: {found_cv_hard + found_cv_soft}
Missing: {missing_hard + missing_soft + missing_lang}
CV: {cv_content[:400]}  Job: {job_desc[:400]}
{depth_instructions[analysis_depth]}
Reply in English. Use emoji headers: 💪 Your Strengths / 🎯 Priority Gaps / 📚 Next Steps"""
            try:
                r = client.models.generate_content(model="gemini-2.0-flash", contents=coach_prompt)
                coach_text = r.text.replace(chr(10), '<br>')
            except Exception as e:
                strengths = ", ".join((found_cv_hard + found_cv_soft)[:5]) or "your existing experience"
                gaps = ", ".join((missing_hard + missing_soft)[:5]) or "the skills listed above"
                coach_text = f"💪 <strong>Your Strengths</strong><br>Solid competencies in {strengths}. {pct_total}% overall match — good foundation.<br><br>🎯 <strong>Priority Gaps</strong><br>Focus on: {gaps}.<br><br>📚 <strong>Next Steps</strong><br>1. Prioritize missing hard skills via online courses.<br>2. Highlight strengths in your CV.<br>3. Connect with people in this role."
        st.markdown(f'<div class="ai-coach-box">{coach_text.strip()}</div>', unsafe_allow_html=True)

        # ── Course Recommender ─────────────────────────────────────────────────
        if missing_hard or missing_soft:
            st.divider()
            st.subheader("🎓 Recommended Courses to Close Your Gaps")

            courses_to_show = []
            unknown_skills = []
            all_missing = (missing_hard + missing_soft)[:8]
            for skill in all_missing:
                if skill in COURSE_DB:
                    courses_to_show.append({"skill": skill, **COURSE_DB[skill]})
                else:
                    unknown_skills.append(skill)

            # For unknown skills, use safe search URLs (no invented direct URLs):
            for skill in unknown_skills:
                platform = "Coursera"
                search_url = f"https://www.coursera.org/search?query={skill.replace(' ', '+')}"
                courses_to_show.append({
                    "skill": skill,
                    "course": f"{skill} — Search Results",
                    "instructor": "Various instructors",
                    "platform": platform,
                    "level": "Beginner",
                    "duration": "varies",
                    "url": search_url
                })

            platform_icons = {"Coursera":"🎓","Udemy":"🎯","LinkedIn Learning":"💼","YouTube":"▶️","edX":"📚"}
            level_colors = {"Beginner":"#2e4d3d","Intermediate":"#c9723a","Advanced":"#c0392b"}

            cols = st.columns(2)
            for i, c in enumerate(courses_to_show):
                level = c.get("level","Beginner")
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="course-card">
                        <div style="margin-bottom:8px;">
                            <span class="course-tag">❌ {c.get('skill','')}</span>
                            <span class="course-tag" style="color:{level_colors.get(level,'#2e4d3d')}">{level}</span>
                            <span class="course-tag">⏱ {c.get('duration','')}</span>
                        </div>
                        <div style="font-weight:700;font-size:15px;color:#2d2d2d;margin-bottom:2px;">{platform_icons.get(c.get('platform',''),'📖')} {c.get('course','')}</div>
                        <div style="font-size:13px;color:#6d6d6d;margin-bottom:10px;">{c.get('instructor','')} · {c.get('platform','')}</div>
                        <a href="{c.get('url','#')}" target="_blank"
                           style="background:#2e4d3d;color:white;padding:6px 16px;border-radius:20px;text-decoration:none;font-size:13px;font-weight:600;">
                            View Course →
                        </a>
                    </div>""", unsafe_allow_html=True)

    else:
        st.error("Missing data: Please provide both your profile (PDF or Text) and the job description.")



# ── Two AI Chat Tabs ───────────────────────────────────────────────────────────
if st.session_state.get("analysis_done"):
    st.divider()
    st.header("🤖 AI Assistants")

    tab1, tab2 = st.tabs(["🎓 Course Finder", "🎤 Interview Prep"])

    # ── TAB 1: Course Finder ───────────────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#2e4d3d,#3d6b52);border-radius:16px;
             padding:20px 24px;margin-bottom:16px;color:white;">
            <h3 style="margin:0 0 4px 0;">🎓 Find Your Perfect Course</h3>
            <p style="margin:0;opacity:0.85;font-size:14px;">
                Click a skill gap below and I'll recommend the best course for your situation.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if "course_chat" not in st.session_state:
            st.session_state["course_chat"] = []
        if "course_selected_skill" not in st.session_state:
            st.session_state["course_selected_skill"] = None
        if "course_time" not in st.session_state:
            st.session_state["course_time"] = None

        missing = st.session_state.get("missing_skills", [])

        # ── Step 1: Skill buttons ──
        if not st.session_state["course_selected_skill"]:
            with st.chat_message("assistant", avatar="🎓"):
                st.markdown(f"👋 I found **{len(missing)} skill gap(s)** for this role. Which one do you want to close first?")
            if missing:
                cols = st.columns(min(len(missing), 4))
                for i, skill in enumerate(missing):
                    with cols[i % 4]:
                        if st.button(skill, key=f"skill_btn_{skill}", use_container_width=True):
                            st.session_state["course_selected_skill"] = skill
                            st.session_state["course_chat"] = [{"role": "user", "content": f"I want to learn {skill}"}]
                            st.rerun()

        # ── Step 2: Time buttons ──
        elif not st.session_state["course_time"]:
            with st.chat_message("assistant", avatar="🎓"):
                st.markdown(f"Great choice! **{st.session_state['course_selected_skill']}** is a high-impact skill for this role. How much time can you dedicate per week?")
            time_options = ["1-2 hours/week", "3-5 hours/week", "5-10 hours/week", "Full-time"]
            cols = st.columns(4)
            for i, t in enumerate(time_options):
                with cols[i]:
                    if st.button(t, key=f"time_btn_{t}", use_container_width=True):
                        st.session_state["course_time"] = t
                        st.session_state["course_chat"].append({"role": "user", "content": f"I have {t} available"})
                        st.rerun()

        # ── Step 3: Show recommendation ──
        else:
            # Render chat history:
            for msg in st.session_state["course_chat"]:
                avatar = "🧑" if msg["role"] == "user" else "🎓"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])

            # Only call API once when we have skill + time but no recommendation yet:
            last_role = st.session_state["course_chat"][-1]["role"] if st.session_state["course_chat"] else None
            if last_role == "user":
                skill = st.session_state["course_selected_skill"]
                time_avail = st.session_state["course_time"]
                course_info = COURSE_DB.get(skill)
                db_line = f"- '{course_info['course']}' by {course_info['instructor']} on {course_info['platform']} ({course_info['level']}, {course_info['duration']}) — {course_info['url']}" if course_info else "Not in database — recommend a real course from Coursera or Udemy."

                prompt = f"""You are a friendly learning advisor.

The candidate wants to learn: {skill}
Their time availability: {time_avail}
Their background: {st.session_state.get('cv_content','')[:200]}
Target role: {st.session_state.get('job_title','')}

Course available in our database for this skill:
{db_line}

Give a warm, specific recommendation (2-3 sentences). Include:
1. Why this course fits their time and background
2. The course name, instructor, platform and direct link
3. One practical tip to get started

Then ask: "Would you like to explore another skill gap?" """

                with st.chat_message("assistant", avatar="🎓"):
                    with st.spinner("Finding the perfect course..."):
                        try:
                            r = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
                            reply = r.text.strip()
                        except Exception as e:
                            reply = f"⚠️ API error: {str(e)}"
                    st.markdown(reply)
                st.session_state["course_chat"].append({"role": "assistant", "content": reply})
                st.rerun()

            # After recommendation: button to start over with another skill
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                remaining = [s for s in missing if s != st.session_state["course_selected_skill"]]
                if remaining:
                    st.markdown("**Want to explore another gap?**")
                    cols = st.columns(min(len(remaining), 4))
                    for i, skill in enumerate(remaining):
                        with cols[i % 4]:
                            if st.button(skill, key=f"skill_again_{skill}", use_container_width=True):
                                st.session_state["course_selected_skill"] = skill
                                st.session_state["course_time"] = None
                                st.session_state["course_chat"] = [{"role": "user", "content": f"I want to learn {skill}"}]
                                st.rerun()

    # ── TAB 2: Interview Prep ──────────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#c9723a,#e08c55);border-radius:16px;
             padding:20px 24px;margin-bottom:16px;color:white;">
            <h3 style="margin:0 0 4px 0;">🎤 Interview Prep Simulator</h3>
            <p style="margin:0;opacity:0.85;font-size:14px;">
                Practice real interview questions and get instant feedback.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if "interview_chat" not in st.session_state:
            st.session_state["interview_chat"] = []
        if "interview_started" not in st.session_state:
            st.session_state["interview_started"] = False
        if "interview_area" not in st.session_state:
            st.session_state["interview_area"] = None

        # ── Step 1: Choose area buttons ──
        if not st.session_state["interview_started"]:
            with st.chat_message("assistant", avatar="🎤"):
                st.markdown(f"""👋 Let's get you ready for your **{st.session_state.get('job_title','target role')}** interview!

I'll ask real questions and give you honest feedback with a ⭐ score after each answer.

**What do you want to practice?**""")

            areas = ["My strengths 💪", "My skill gaps 🎯", "Behavioural questions 🧠", "Mix of everything 🎲"]
            cols = st.columns(2)
            for i, area in enumerate(areas):
                with cols[i % 2]:
                    if st.button(area, key=f"area_{area}", use_container_width=True):
                        st.session_state["interview_area"] = area
                        st.session_state["interview_started"] = True
                        st.session_state["interview_chat"] = [{"role": "user", "content": f"I want to practice: {area}"}]
                        st.rerun()

        # ── Step 2: Active interview ──
        else:
            for msg in st.session_state["interview_chat"]:
                avatar = "🧑" if msg["role"] == "user" else "🎤"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])

            # If last message is from user, get interviewer response:
            last_role = st.session_state["interview_chat"][-1]["role"] if st.session_state["interview_chat"] else None
            if last_role == "user":
                history_text = "\n".join([
                    f"{'Candidate' if m['role']=='user' else 'Interviewer'}: {m['content']}"
                    for m in st.session_state["interview_chat"]
                ])
                interview_prompt = f"""You are a professional interviewer AND coach.

CANDIDATE PROFILE:
- Target role: {st.session_state.get('job_title','')}
- Strong skills: {st.session_state.get('found_cv',[])}
- Skill gaps: {st.session_state.get('missing_skills',[])}
- CV: {st.session_state.get('cv_content','')[:250]}
- Practice area chosen: {st.session_state.get('interview_area','')}

RULES:
1. First message after area selection: ask ONE real interview question immediately
2. If candidate answered a question: score 1-5 ⭐, give specific feedback, show a stronger example answer in italics
3. Then ask the next question automatically (don't wait for them to ask)
4. Keep questions specific to this role and their profile
5. Be encouraging but honest

CONVERSATION:
{history_text}

Interviewer:"""

                with st.chat_message("assistant", avatar="🎤"):
                    with st.spinner("Evaluating..."):
                        try:
                            r = client.models.generate_content(model="gemini-2.0-flash", contents=interview_prompt)
                            reply = r.text.strip()
                        except Exception as e:
                            reply = f"⚠️ API error: {str(e)}"
                    st.markdown(reply)
                st.session_state["interview_chat"].append({"role": "assistant", "content": reply})
                st.rerun()

            # If last message is from assistant: show text input to answer
            else:
                answer = st.chat_input("Type your answer...", key="interview_input")
                if answer:
                    st.session_state["interview_chat"].append({"role": "user", "content": answer})
                    st.rerun()

                # Also offer quick action buttons:
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("⏭ Next question", use_container_width=True):
                        st.session_state["interview_chat"].append({"role": "user", "content": "Next question please"})
                        st.rerun()
                with col2:
                    if st.button("🔄 Change area", use_container_width=True):
                        st.session_state["interview_started"] = False
                        st.session_state["interview_chat"] = []
                        st.rerun()
                with col3:
                    if st.button("🗑 Start over", use_container_width=True):
                        st.session_state["interview_started"] = False
                        st.session_state["interview_chat"] = []
                        st.session_state["interview_area"] = None
                        st.rerun()
                        