import streamlit as st
import time

#Browser tab:
st.set_page_config(page_title="Skill-gap analyzer", layout="wide")

#Background:
st.markdown("""
    <style>
        .stApp {
            background-color: #f2ede4;
        }

        .main-header {
            background: linear-gradient(135deg, #fcebdb 0%, #f7d7be 100%);
            padding: 40px;
            border-radius: 40px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }

        [data-testid="stVerticalBlock"] > div:has(div[data-testid="stVerticalBlock"]) {
            background-color: #faf8f5;
            padding: 25px;
            border-radius: 30px 30px 80px 30px;
            box-shadow: 5px 5px 20px rgba(0,0,0,0.02);
            border: 1px solid #ffffff;
            margin-bottom: 20px;
        }

        .stButton>button {
            background-color: #e68a4d;
            color: white;
            border-radius: 20px;
            border: none;
            padding: 10px 25px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #d3753b;
            transform: scale(1.02);
        }

        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 15px;
            border: 1px solid #e0d9ce;
            background-color: #ffffff;
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
        <p style="color: #6d6d6d; font-size: 18px;">AI-powered professional benchmarking & career roadmap.</p>
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

        # Logic to find matches
        file_name = uploaded_cv.name if uploaded_cv else ""
        cv_content = (cv_text if cv_text else "") + " " + file_name

        found_cv = [s for s in hard_skills + soft_skills + languages if s.lower() in cv_content.lower()]
        found_jd = [s for s in hard_skills + soft_skills + languages if s.lower() in job_desc.lower()]
        missing_skills = [s for s in found_jd if s not in found_cv]

        # 7. Results Section
        st.divider()
        st.header("📊 Detailed Skill Analysis")

        # Checklist
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
                st.success("You have all the required skills mentioned in the JD!")

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
            color=["#e68a4d", "#2d2d2d"], # Matched to our Burnt Orange and Dark Grey theme
            stack=False
        )
        
    else:
        st.error("Missing data: Please provide both your profile (PDF or Text) and the job description.")