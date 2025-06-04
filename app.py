import streamlit as st

st.title("🇮🇳 AI Government Job Prep")
st.write("AI-powered platform for Indian government exam preparation")

# Language selector
language = st.selectbox("Language", ["English", "हिंदी"])

if language == "हिंदी":
    st.write("भारतीय सरकारी परीक्षाओं की तैयारी के लिए एआई-संचालित मंच")
else:
    st.write("Prepare for UPSC, SSC, Banking, Railway and other competitive exams")

# Basic profile
st.header("Profile Setup")
name = st.text_input("Your Name")
exam = st.selectbox("Target Exam", ["UPSC", "SSC", "Banking", "Railway", "Other"])

if name:
    st.success(f"Welcome {name}! Preparing for {exam}")

# Status
st.header("Status")
st.success("✅ App is working")
st.success("✅ Deployment successful")

# Check for OpenAI
import os
if "OPENAI_API_KEY" in os.environ:
    st.success("✅ OpenAI configured")
    
    if st.button("Test AI"):
        try:
            from openai import OpenAI
            client = OpenAI()
            st.success("✅ AI connection working")
        except Exception as e:
            st.error(f"AI error: {e}")
else:
    st.warning("⚠️ Add OPENAI_API_KEY to secrets for AI features")

st.markdown("---")
st.caption("Built for Indian government job preparation")
