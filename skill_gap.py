import streamlit as st
import time
import json
import re
from google import genai

#Browser tab:
st.set_page_config(page_title="Skill-gap analyzer", layout="wide")

#Gemini setup:
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

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

        /* 2. RADIO BUTTONS */
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

        /* 3. PROGRESS BAR */
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

        /* 5. INFO BOX */
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

        /* 6. TEXT AREA & TEXT INPUT */
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

        /* 7. FILE UPLOADER */
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

        /* 9. AI COACH BOX */
        .ai-coach-box {
            background: linear-gradient(135deg, #faf8f5 0%, #fdf3e7 100%);
            border: 1px solid #e8ddd0;
            border-left: 4px solid #2e4d3d;
            border-radius: 16px;
            padding: 28px 32px;
            margin-top: 8px;
            color: #2d2d2d;
            font-size: 15px;
            line-height: 1.7;
        }

        /* 10. COURSE CARDS */
        .course-card {
            background: #faf8f5;
            border: 1px solid #e8ddd0;
            border-radius: 16px;
            padding: 18px 20px;
            margin-bottom: 12px;
            transition: border-color 0.2s;
        }
        .course-card:hover {
            border-color: #c9723a;
        }
        .course-tag {
            display: inline-block;
            background: #fdf3e7;
            border: 1px solid #e8ddd0;
            border-radius: 20px;
            padding: 2px 10px;
            font-size: 12px;
            color: #c9723a;
            font-weight: 600;
            margin-right: 6px;
        }

        /* 11. CHAT MESSAGES */
        .chat-user {
            background: #2e4d3d;
            color: white;
            border-radius: 16px 16px 4px 16px;
            padding: 12px 18px;
            margin: 8px 0 8px 20%;
            font-size: 14px;
            line-height: 1.6;
        }
        .chat-bot {
            background: #faf8f5;
            border: 1px solid #e8ddd0;
            border-radius: 16px 16px 16px 4px;
            padding: 12px 18px;
            margin: 8px 20% 8px 0;
            font-size: 14px;
            line-height: 1.6;
            color: #2d2d2d;
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

        # Progress bar:
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.info("Analyzing compatibility and identifying skill gaps...")
        for percent_complete in range(60):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)

        # PDF reading + text input:
        file_name = uploaded_cv.name if uploaded_cv else ""
        pdf_text = ""
        if uploaded_cv:
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(uploaded_cv)
                for page in reader.pages:
                    pdf_text += page.extract_text() or ""
            except Exception as e:
                st.warning(f"Could not read PDF text: {e}")

        # Clean and normalize extracted text:
        pdf_text = re.sub(r'\s+', ' ', pdf_text)
        pdf_text = pdf_text.replace('PowerBI', 'Power BI').replace('powerbi', 'Power BI')
        cv_content = (cv_text if cv_text else "") + " " + pdf_text + " " + file_name

        # Aliases for flexible matching:
        aliases = {
            "Power BI": ["PowerBI", "powerbi", "power bi"],
            "Machine Learning": ["machine learning", "ML", "ml"],
            "Data Visualization": ["data visualization", "data viz", "dataviz"],
            "Communication": ["communicating", "communications"],
            "Critical Thinking": ["critical thinking", "critical-thinking"],
            "Presentation": ["presentations", "presenting"],
            "Statistics": ["statistical", "stats"],
            "Python": ["python"], "SQL": ["sql"], "Tableau": ["tableau"],
            "AWS": ["aws", "amazon web services"], "Excel": ["excel"],
            "Agile": ["agile", "agile methodologies"],
            "Leadership": ["leadership", "leading", "led"],
            "Teamwork": ["teamwork", "team work", "cross-functional"],
            "Project Management": ["project management", "managing projects"],
        }
        cv_expanded = cv_content.lower()
        canonical_injections = []
        for canonical, variants in aliases.items():
            for variant in variants:
                if variant.lower() in cv_expanded:
                    canonical_injections.append(canonical)
                    break
        cv_content = cv_content + " " + " ".join(canonical_injections)

        depth_instructions = {
            "Fast":     "Be concise. Give a brief 2-3 sentence summary only.",
            "Standard": "Give a balanced analysis with key points and actionable advice.",
            "Detailed": "Give an in-depth analysis with specific examples, priorities, and a step-by-step action plan."
        }

        # Skill dictionaries:
        hard_skills = [
            "Python", "SQL", "Excel", "Tableau", "Power BI", "Statistics", "Machine Learning",
            "R", "Git", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib",
            "Deep Learning", "NLP", "Computer Vision", "Data Visualization", "Big Data", "Spark",
            "Hadoop", "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Java", "JavaScript",
            "TypeScript", "React", "Node.js", "HTML", "CSS", "MongoDB", "PostgreSQL", "MySQL",
            "Airflow", "dbt", "Looker", "Snowflake", "Databricks", "Kafka", "API", "REST",
            "A/B Testing", "Forecasting", "Regression", "Classification", "Clustering", "Excel VBA",
            "SPSS", "SAS", "Matlab", "Scala", "ETL", "Data Engineering", "MLOps", "CI/CD"
        ]
        soft_skills = [
            "Leadership", "Communication", "Teamwork", "Agile", "Management", "Problem Solving",
            "Critical Thinking", "Creativity", "Collaboration", "Adaptability", "Time Management",
            "Project Management", "Scrum", "Kanban", "Stakeholder Management", "Presentation",
            "Negotiation", "Mentoring", "Strategic Thinking", "Decision Making", "Analytical Thinking",
            "Attention to Detail", "Customer Focus", "Innovation", "Conflict Resolution"
        ]
        languages = [
            "English", "Spanish", "French", "German", "Italian", "Portuguese", "Chinese",
            "Mandarin", "Japanese", "Arabic", "Dutch", "Russian", "Korean", "Swedish", "Catalan"
        ]

        # Keyword matching:
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

        # Save analysis context in session state for the chatbot:
        st.session_state["analysis_done"] = True
        st.session_state["cv_content"] = cv_content
        st.session_state["job_desc"] = job_desc
        st.session_state["job_title"] = job_title
        st.session_state["found_cv"] = found_cv
        st.session_state["missing_skills"] = missing_skills
        st.session_state["chat_history"] = []

        for percent_complete in range(60, 100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)

        status_text.success("Analysis complete!")

        st.divider()
        st.header("📊 Detailed Skill Analysis")

        # Percentages:
        def match_pct(cv_list, jd_list):
            if not jd_list:
                return 100
            matched = len([s for s in jd_list if s in cv_list])
            return round((matched / len(jd_list)) * 100)

        pct_hard  = match_pct(found_cv_hard, found_jd_hard)
        pct_soft  = match_pct(found_cv_soft, found_jd_soft)
        pct_lang  = match_pct(found_cv_lang, found_jd_lang)
        pct_total = match_pct(found_cv, found_jd)

        def color_for(pct):
            if pct >= 75: return "#2e4d3d"
            if pct >= 40: return "#c9723a"
            return "#c0392b"

        # Donuts SVG:
        def donut_html(pct, label, size=160):
            r = 54
            circ = 2 * 3.14159 * r
            fill   = round((pct / 100) * circ, 1)
            gap    = round(circ - fill, 1)
            col    = color_for(pct)
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

        circ_total   = 2 * 3.14159 * 54
        fill_total   = round((pct_total / 100) * circ_total, 1)
        gap_total    = round(circ_total - fill_total, 1)
        offset_total = round(circ_total / 4, 1)
        col_total    = color_for(pct_total)

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
                        <span style="font-size:18px;">✅</span>
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
                        <span style="font-size:18px;">❌</span>
                        <span style="font-weight:600;color:#1a1a1a;">{skill}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background-color:#2e4d3d;color:white;padding:10px;border-radius:10px;text-align:center;font-weight:bold;">
                    🌟 You have all the required skills!
                    </div>
                """, unsafe_allow_html=True)

        # AI Career Coach:
        st.divider()
        st.subheader("🤖 AI Career Coach")
        with st.spinner("Generating your personalized career advice..."):
            coach_prompt = f"""Career coach. Skill gap analysis results:
Match: {pct_total}% overall, {pct_hard}% hard skills, {pct_soft}% soft skills, {pct_lang}% languages.
Strong skills: {found_cv_hard + found_cv_soft}
Missing: {missing_hard + missing_soft + missing_lang}
CV summary: {cv_content[:400]}
Job: {job_desc[:400]}
{depth_instructions[analysis_depth]}
Reply in English to the candidate. Use emoji headers: 💪 Your Strengths / 🎯 Priority Gaps / 📚 Next Steps"""
            try:
                coach_response = client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=coach_prompt
                )
                coach_text = coach_response.text.replace(chr(10), '<br>')
            except Exception:
                strengths = ", ".join((found_cv_hard + found_cv_soft)[:5]) or "your existing experience"
                gaps = ", ".join((missing_hard + missing_soft)[:5]) or "the specific skills listed above"
                coach_text = f"""
💪 <strong>Your Strengths</strong><br>
Your profile shows solid competencies in {strengths}.
With a {pct_total}% overall match, you have a good foundation for this role.<br><br>
🎯 <strong>Priority Gaps to Close</strong><br>
Focus on developing: {gaps}.
These are the key areas where the job requirements go beyond your current profile.<br><br>
📚 <strong>Recommended Next Steps</strong><br>
1. Prioritize the missing hard skills through online courses or hands-on projects.<br>
2. Highlight your existing strengths clearly in your CV and cover letter.<br>
3. Consider reaching out to people in this role to better understand day-to-day requirements.
"""
        st.markdown(f"""
        <div class="ai-coach-box">
            {coach_text.strip()}
        </div>
        """, unsafe_allow_html=True)

        # ── FEATURE 1: Course Recommender ──────────────────────────────────────
        if missing_hard or missing_soft:
            st.divider()
            st.subheader("🎓 Recommended Courses to Close Your Gaps")
            with st.spinner("Finding the best courses for your skill gaps..."):
                course_prompt = f"""You are a learning advisor. A candidate is missing these skills for a job:
Hard skills missing: {missing_hard[:6]}
Soft skills missing: {missing_soft[:4]}
Job title: {job_title or "the target role"}

Return ONLY a JSON array with exactly {min(len(missing_hard[:6]) + len(missing_soft[:4]), 6)} objects. No extra text, no markdown.
Each object must have these exact keys:
- "skill": the skill name
- "course": specific course title
- "platform": one of Coursera, Udemy, LinkedIn Learning, YouTube, edX
- "level": one of Beginner, Intermediate, Advanced
- "duration": estimated duration (e.g. "6 hours", "4 weeks")
- "url": a plausible URL to the course (e.g. https://www.coursera.org/learn/course-name)

Prioritize the most impactful skills first. Make course titles realistic and specific."""

                try:
                    course_response = client.models.generate_content(
                        model="gemini-2.0-flash-lite",
                        contents=course_prompt
                    )
                    raw = course_response.text.strip()
                    raw = re.sub(r"```json|```", "", raw).strip()
                    courses = json.loads(raw)
                except Exception:
                    # Fallback static courses if API fails:
                    courses = [
                        {"skill": s, "course": f"Introduction to {s}", "platform": "Coursera",
                         "level": "Beginner", "duration": "6 hours",
                         "url": f"https://www.coursera.org/search?query={s.replace(' ', '+')}"}
                        for s in (missing_hard + missing_soft)[:6]
                    ]

            # Render course cards in 2 columns:
            platform_icons = {
                "Coursera": "🎓", "Udemy": "🎯", "LinkedIn Learning": "💼",
                "YouTube": "▶️", "edX": "📚"
            }
            level_colors = {
                "Beginner": "#2e4d3d", "Intermediate": "#c9723a", "Advanced": "#c0392b"
            }

            cols = st.columns(2)
            for i, course in enumerate(courses):
                icon = platform_icons.get(course.get("platform", ""), "📖")
                level = course.get("level", "Beginner")
                lvl_color = level_colors.get(level, "#2e4d3d")
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="course-card">
                        <div style="margin-bottom:8px;">
                            <span class="course-tag">❌ {course.get('skill','')}</span>
                            <span class="course-tag" style="color:{lvl_color};">{level}</span>
                            <span class="course-tag">⏱ {course.get('duration','')}</span>
                        </div>
                        <div style="font-weight:700;font-size:15px;color:#2d2d2d;margin-bottom:4px;">
                            {icon} {course.get('course','')}
                        </div>
                        <div style="font-size:13px;color:#6d6d6d;margin-bottom:10px;">
                            {course.get('platform','')}
                        </div>
                        <a href="{course.get('url','#')}" target="_blank"
                           style="background:#2e4d3d;color:white;padding:6px 16px;border-radius:20px;
                                  text-decoration:none;font-size:13px;font-weight:600;">
                            View Course →
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

    else:
        st.error("Missing data: Please provide both your profile (PDF or Text) and the job description.")

# ── FEATURE 2: Career Coach Chatbot ────────────────────────────────────────────
if st.session_state.get("analysis_done"):
    st.divider()
    st.subheader("💬 Chat with your Career Coach")
    st.caption("Ask anything about your results, how to improve, or how to prepare for interviews.")

    # Display chat history:
    for msg in st.session_state.get("chat_history", []):
        css_class = "chat-user" if msg["role"] == "user" else "chat-bot"
        st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

    # Chat input:
    user_input = st.chat_input("Ask your career coach...")
    if user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        # Build system context + full conversation history for multi-call:
        system_context = f"""You are a friendly, expert career coach. You have already analyzed this candidate's profile.
CV summary: {st.session_state.get('cv_content','')[:300]}
Target job: {st.session_state.get('job_title','')} — {st.session_state.get('job_desc','')[:300]}
Skills they have: {st.session_state.get('found_cv',[])}
Skills they are missing: {st.session_state.get('missing_skills',[])}
Answer in English, be concise, encouraging and practical. Max 3 short paragraphs."""

        # Build full conversation for Gemini multi-turn:
        conversation = system_context + "\n\n"
        for msg in st.session_state["chat_history"]:
            role = "Candidate" if msg["role"] == "user" else "Coach"
            conversation += f"{role}: {msg['content']}\n"
        conversation += "Coach:"

        try:
            chat_response = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=conversation
            )
            bot_reply = chat_response.text.strip()
        except Exception:
            bot_reply = "I'm having trouble connecting right now. Please try again in a moment!"

        st.session_state["chat_history"].append({"role": "assistant", "content": bot_reply})
        st.rerun()
