import streamlit as st
import time

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