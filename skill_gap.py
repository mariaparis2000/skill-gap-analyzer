import streamlit as st
import time
import json
import re
from groq import Groq

# Centralized Model Configuration
MAIN_MODEL = "llama-3.3-70b-versatile"
CHAT_MODEL = "llama-3.1-8b-instant"

st.set_page_config(page_title="Skill-gap analyzer", layout="wide")

# Initialize Groq Client
try:
    groq_api_key = st.secrets.get("GROQ_API_KEY") or st.secrets.get("groq_api_key")
    client = Groq(api_key=groq_api_key)
except Exception as e:
    st.error(f"⚠️ Error loading Groq API key: {str(e)}")
    st.stop()

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        .stApp { background-color: #f2ede4; }
        .main-header {
            background: linear-gradient(135deg, #fcebdb 0%, #f7d7be 100%);
            padding: 40px; border-radius: 40px; text-align: center; margin-bottom: 30px;
        }
        .ai-coach-box {
            background: linear-gradient(135deg, #faf8f5 0%, #fdf3e7 100%);
            border: 1px solid #e8ddd0; border-left: 4px solid #2e4d3d;
            border-radius: 16px; padding: 28px 32px; margin-top: 20px;
            color: #2d2d2d; font-size: 15px; line-height: 1.7;
        }
        .section-title {
            color: white; padding: 12px; border-radius: 12px 12px 0 0; 
            font-weight: bold; text-align: center; margin-bottom: 0px;
        }
    </style>
""", unsafe_allow_html=True)

# ── Helper Functions for Visuals ──────────────────────────────────────────────
def color_for(pct):
    if pct >= 75: return "#2e4d3d"
    if pct >= 40: return "#c9723a"
    return "#c0392b"

def donut_html(pct, label, size=150):
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
        <span style="font-size:13px;font-weight:600;color:#2d2d2d;">{label}</span>
    </div>"""

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.title("Configuration")
analysis_depth = st.sidebar.radio("Analysis Depth:", options=["Fast", "Standard", "Detailed"], index=1, horizontal=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="main-header">
        <h1 style="color:#2d2d2d;font-size:45px;margin-bottom:0;">Skill-Gap Analyzer</h1>
        <p style="color:#6d6d6d;font-size:18px;">Your command center for career success.</p>
    </div>
""", unsafe_allow_html=True)

# ── Inputs ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📝 Your Profile")
    uploaded_cv = st.file_uploader("Upload CV (PDF)", type="pdf")
    cv_text_manual = st.text_area("Or paste skills/summary:", height=100)
with col2:
    st.markdown("### 💼 Target Job")
    job_title = st.text_input("Job Title", placeholder="e.g. Data Scientist")
    job_desc = st.text_area("Requirements:", height=100)

# ── Analysis Logic ─────────────────────────────────────────────────────────────
if st.button("🚀 Start Match Analysis", use_container_width=True):
    if (uploaded_cv or cv_text_manual) and job_desc:
        cv_raw = cv_text_manual if cv_text_manual else ""
        if uploaded_cv:
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded_cv)
            for page in reader.pages:
                cv_raw += page.extract_text() or ""
        
        cv_clean = cv_raw.lower()
        jd_clean = job_desc.lower()

        hard_skills = [
            "Python","SQL","Excel","Tableau","Power BI","Statistics","Machine Learning","R","Git","TensorFlow",
            "PyTorch","Scikit-learn","Pandas","NumPy","Matplotlib","Deep Learning","NLP","Computer Vision",
            "Data Visualization","Big Data","Spark","Hadoop","AWS","Azure","GCP","Docker","Kubernetes","Java",
            "JavaScript","TypeScript","React","Node.js","HTML","CSS","MongoDB","PostgreSQL","MySQL","Airflow",
            "dbt","Looker","Snowflake","Databricks","Kafka","API","REST","A/B Testing","Forecasting","Regression",
            "Classification","Clustering","ETL","Data Engineering","MLOps","CI/CD"
        ]
        soft_skills = [
            "Leadership","Communication","Teamwork","Agile","Management","Problem Solving","Critical Thinking",
            "Creativity","Collaboration","Adaptability","Time Management","Project Management","Scrum","Kanban",
            "Stakeholder Management","Presentation","Negotiation","Mentoring"
        ]
        languages = ["English","Spanish","French","German","Italian","Chinese","Japanese","Portuguese","Russian"]

        def detect_skills(text, skill_list):
            detected = []
            for skill in skill_list:
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text):
                    detected.append(skill)
            return detected

        found_cv_h = detect_skills(cv_clean, hard_skills)
        found_cv_s = detect_skills(cv_clean, soft_skills)
        found_cv_l = detect_skills(cv_clean, languages)
        
        found_jd_h = detect_skills(jd_clean, hard_skills)
        found_jd_s = detect_skills(jd_clean, soft_skills)
        found_jd_l = detect_skills(jd_clean, languages)
        
        def calc_pct(found_in_cv, found_in_jd):
            if not found_in_jd: return 100
            matches = [s for s in found_in_jd if s in found_in_cv]
            return min(round(len(matches) / len(found_in_jd) * 100), 100)

        st.session_state["analysis_done"] = True
        st.session_state["job_title"] = job_title
        st.session_state["cv_raw"] = cv_raw
        st.session_state["job_desc"] = job_desc
        st.session_state["found_cv"] = found_cv_h + found_cv_s + found_cv_l
        st.session_state["missing_skills"] = [s for s in (found_jd_h + found_jd_s + found_jd_l) if s not in (found_cv_h + found_cv_s + found_cv_l)]
        st.session_state["pct_h"] = calc_pct(found_cv_h, found_jd_h)
        st.session_state["pct_s"] = calc_pct(found_cv_s, found_jd_s)
        st.session_state["pct_l"] = calc_pct(found_cv_l, found_jd_l)
        
        # Reset States
        st.session_state["course_chat"] = []
        st.session_state["course_selected_skill"] = None
        st.session_state["course_time"] = None
        st.session_state["interview_chat"] = []
        st.session_state["interview_started"] = False
        st.session_state["interview_area"] = None
        st.rerun()

# ── Results Dashboard ──────────────────────────────────────────────────────────
if st.session_state.get("analysis_done"):
    st.divider()
    
    st.subheader("📊 Match Analysis")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(donut_html(st.session_state["pct_h"], "Hard Skills"), unsafe_allow_html=True)
    with c2: st.markdown(donut_html(st.session_state["pct_s"], "Soft Skills"), unsafe_allow_html=True)
    with c3: st.markdown(donut_html(st.session_state["pct_l"], "Languages"), unsafe_allow_html=True)
    with c4: st.metric("Gaps Found", len(st.session_state["missing_skills"]))

    st.divider()

    col_left, col_right = st.columns(2)

    # --- LEFT: GUIDED COURSE FINDER ---
    with col_left:
        st.markdown('<div class="section-title" style="background:#2e4d3d;">🎓 Guided Course Finder</div>', unsafe_allow_html=True)
        with st.container(border=True):
            missing = st.session_state["missing_skills"]
            if not st.session_state["course_selected_skill"]:
                st.write("**Step 1: Which gap do you want to close?**")
                if missing:
                    for s in missing:
                        if st.button(f"Focus on {s}", key=f"course_btn_{s}", use_container_width=True):
                            st.session_state["course_selected_skill"] = s
                            st.rerun()
                else:
                    st.success("Perfect match! No gaps detected.")
            elif not st.session_state["course_time"]:
                st.write(f"**Step 2: How much time per week for {st.session_state['course_selected_skill']}?**")
                for t in ["1-2 hours", "3-5 hours", "10+ hours"]:
                    if st.button(t, key=f"time_btn_{t}", use_container_width=True):
                        st.session_state["course_time"] = t
                        st.rerun()
            else:
                for msg in st.session_state["course_chat"]:
                    with st.chat_message(msg["role"]): st.write(msg["content"])
                if not st.session_state["course_chat"]:
                    with st.spinner("Finding best course..."):
                        prompt = f"Recommend a real online course for {st.session_state['course_selected_skill']} for a {st.session_state['job_title']} role. Availability: {st.session_state['course_time']}. Provide links."
                        resp = client.chat.completions.create(model=CHAT_MODEL, messages=[{"role": "user", "content": prompt}])
                        st.session_state["course_chat"].append({"role": "assistant", "content": resp.choices[0].message.content})
                        st.rerun()
                if st.button("🔄 Pick another skill"):
                    st.session_state["course_selected_skill"], st.session_state["course_time"], st.session_state["course_chat"] = None, None, []
                    st.rerun()

    # --- RIGHT: INTERVIEW SIMULATOR (WITH INITIAL BUTTONS) ---
    with col_right:
        st.markdown('<div class="section-title" style="background:#c9723a;">🎤 Interview Simulator</div>', unsafe_allow_html=True)
        with st.container(border=True):
            if not st.session_state.get("interview_started"):
                st.write("**What do you want to practice today?**")
                areas = ["My strengths 💪", "My skill gaps 🎯", "Behavioral questions 🧠", "Mix of everything 🎲"]
                for area in areas:
                    if st.button(area, key=f"int_area_{area}", use_container_width=True):
                        st.session_state["interview_area"] = area
                        st.session_state["interview_started"] = True
                        st.session_state["interview_chat"] = []
                        st.rerun()
            else:
                for msg in st.session_state["interview_chat"]:
                    with st.chat_message(msg["role"]): st.write(msg["content"])
                
                if not st.session_state["interview_chat"]:
                    with st.spinner("Starting interview..."):
                        prompt = f"Start an interview for {st.session_state['job_title']} focusing on {st.session_state['interview_area']}. Ask the first question."
                        resp = client.chat.completions.create(model=CHAT_MODEL, messages=[{"role": "user", "content": prompt}])
                        st.session_state["interview_chat"].append({"role": "assistant", "content": resp.choices[0].message.content})
                        st.rerun()

                ans = st.chat_input("Your answer...", key="int_input_box")
                if ans:
                    st.session_state["interview_chat"].append({"role": "user", "content": ans})
                    prompt = f"Role: {st.session_state['job_title']}. Practice: {st.session_state['interview_area']}. Feedback on: '{ans}'. Score 1-5, suggest improvement, and ask the next question."
                    resp = client.chat.completions.create(model=CHAT_MODEL, messages=[{"role": "user", "content": prompt}])
                    st.session_state["interview_chat"].append({"role": "assistant", "content": resp.choices[0].message.content})
                    st.rerun()
                
                if st.button("🔄 Reset Interview"):
                    st.session_state["interview_started"], st.session_state["interview_chat"] = False, []
                    st.rerun()

    # 3. AI CAREER COACH (Bottom)
    st.divider()
    st.subheader("🤖 AI Career Coach")
    coach_prompt = f"Role: {st.session_state['job_title']}. Found: {st.session_state['found_cv']}. Gaps: {st.session_state['missing_skills']}. Give 3 specific career strategy tips."
    with st.spinner("Analyzing strategy..."):
        resp = client.chat.completions.create(model=MAIN_MODEL, messages=[{"role": "user", "content": coach_prompt}])
        st.markdown(f'<div class="ai-coach-box"><strong>Expert Strategy:</strong><br><br>{resp.choices[0].message.content}</div>', unsafe_allow_html=True)