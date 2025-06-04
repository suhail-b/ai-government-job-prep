import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="AI Government Job Prep",
    page_icon="🇮🇳",
    layout="wide"
)

# Check dependencies
try:
    import openai
    from openai import OpenAI
    openai_available = True
except ImportError:
    openai_available = False

try:
    from streamlit_option_menu import option_menu
    menu_available = True
except ImportError:
    menu_available = False

# CSS for Indian flag theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%);
        padding: 1rem;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: #262730;
        font-weight: bold;
        margin: 0;
    }
    .stButton > button {
        background: linear-gradient(45deg, #FF9933, #138808);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'name': '',
        'exam_type': '',
        'quiz_scores': [],
        'total_points': 0
    }

# Language toggle
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    language = st.selectbox(
        "Language / भाषा",
        options=['en', 'hi'],
        format_func=lambda x: "English" if x == 'en' else "हिंदी"
    )
    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()

# Main header
if st.session_state.language == 'hi':
    header = "एआई सरकारी नौकरी तैयारी"
    welcome = "एआई-संचालित सरकारी नौकरी तैयारी में आपका स्वागत है"
    description = "भारतीय सरकारी परीक्षाओं की तैयारी के लिए एआई-संचालित प्लेटफॉर्म"
else:
    header = "AI Government Job Prep"
    welcome = "Welcome to AI-Powered Government Job Preparation"
    description = "AI-powered platform for Indian government exam preparation"

st.markdown(f'<div class="main-header"><h1>🇮🇳 {header}</h1></div>', unsafe_allow_html=True)

# Navigation
if menu_available:
    if st.session_state.language == 'hi':
        menu_options = ["होम", "एआई क्विज़", "स्थिति"]
    else:
        menu_options = ["Home", "AI Quiz", "Status"]
    
    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=["house", "question-circle", "info-circle"],
        default_index=0,
        orientation="horizontal"
    )
else:
    selected = st.selectbox("Navigation", ["Home", "AI Quiz", "Status"])

# Page content
if selected in ["Home", "होम"]:
    st.markdown(f"## {welcome}")
    st.markdown(description)
    
    # Profile setup
    if st.session_state.language == 'hi':
        profile_text = "प्रोफाइल सेटअप"
        name_text = "आपका नाम"
        exam_text = "लक्षित परीक्षा"
        save_text = "सेव करें"
        saved_text = "प्रोफाइल सेव हो गया!"
    else:
        profile_text = "Profile Setup"
        name_text = "Your Name"
        exam_text = "Target Exam"
        save_text = "Save Profile"
        saved_text = "Profile saved!"
    
    with st.expander(profile_text, expanded=not st.session_state.user_data['name']):
        name = st.text_input(name_text, value=st.session_state.user_data['name'])
        exam_type = st.selectbox(exam_text, [
            'UPSC Civil Services',
            'SSC CGL',
            'Banking',
            'Railway',
            'Other'
        ])
        
        if st.button(save_text):
            st.session_state.user_data['name'] = name
            st.session_state.user_data['exam_type'] = exam_type
            st.success(saved_text)
            st.rerun()
    
    # Stats display
    if st.session_state.user_data['name']:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.language == 'hi':
                st.metric("कुल अंक", st.session_state.user_data['total_points'])
            else:
                st.metric("Total Points", st.session_state.user_data['total_points'])
        with col2:
            if st.session_state.language == 'hi':
                st.metric("पूर्ण क्विज़", len(st.session_state.user_data['quiz_scores']))
            else:
                st.metric("Quizzes Completed", len(st.session_state.user_data['quiz_scores']))
        with col3:
            if st.session_state.user_data['quiz_scores']:
                avg_score = sum(st.session_state.user_data['quiz_scores']) / len(st.session_state.user_data['quiz_scores'])
                if st.session_state.language == 'hi':
                    st.metric("औसत स्कोर", f"{avg_score:.1f}%")
                else:
                    st.metric("Average Score", f"{avg_score:.1f}%")

elif selected in ["AI Quiz", "एआई क्विज़"]:
    if st.session_state.language == 'hi':
        quiz_title = "एआई क्विज़ जेनरेटर"
        topic_text = "विषय चुनें"
        diff_text = "कठिनाई स्तर"
        gen_text = "क्विज़ जेनरेट करें"
        no_api_text = "OpenAI API key की आवश्यकता है"
    else:
        quiz_title = "AI Quiz Generator"
        topic_text = "Select Topic"
        diff_text = "Difficulty Level"
        gen_text = "Generate Quiz"
        no_api_text = "OpenAI API key required"
    
    st.markdown(f"## 📝 {quiz_title}")
    
    if not openai_available:
        st.error("OpenAI package not available")
        st.stop()
    
    # Check for API key
    if "OPENAI_API_KEY" not in os.environ:
        st.warning(no_api_text)
        st.info("Please add your OpenAI API key in the app secrets.")
        st.stop()
    
    # Quiz configuration
    topics = {
        'General Knowledge': 'सामान्य ज्ञान' if st.session_state.language == 'hi' else 'General Knowledge',
        'Indian History': 'भारतीय इतिहास' if st.session_state.language == 'hi' else 'Indian History',
        'Geography': 'भूगोल' if st.session_state.language == 'hi' else 'Geography',
        'Current Affairs': 'समसामयिकी' if st.session_state.language == 'hi' else 'Current Affairs'
    }
    
    selected_topic = st.selectbox(topic_text, list(topics.keys()))
    difficulty = st.slider(diff_text, 1, 5, 3)
    
    if st.button(f"🚀 {gen_text}"):
        try:
            client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            
            lang_instruction = "in Hindi" if st.session_state.language == 'hi' else "in English"
            
            prompt = f"""Generate 3 multiple choice questions for Indian government exams on {selected_topic} {lang_instruction}.
            Return as JSON: {{"questions": [{{"question": "text", "options": ["A", "B", "C", "D"], "correct_answer": 0, "explanation": "text"}}]}}"""
            
            with st.spinner("Generating questions..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert in Indian government job preparation."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
            
            import json
            result = json.loads(response.choices[0].message.content)
            questions = result.get("questions", [])
            
            if questions:
                st.session_state.current_quiz = questions
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.success("Questions generated successfully!")
                st.rerun()
            
        except Exception as e:
            st.error(f"Error generating quiz: {str(e)}")
    
    # Display quiz questions
    if 'current_quiz' in st.session_state:
        quiz = st.session_state.current_quiz
        idx = st.session_state.quiz_index
        
        if idx < len(quiz):
            question = quiz[idx]
            st.markdown(f"### Question {idx + 1}/{len(quiz)}")
            st.markdown(f"**{question['question']}**")
            
            answer = st.radio(
                "Select answer:",
                range(len(question['options'])),
                format_func=lambda x: f"{chr(65+x)}. {question['options'][x]}"
            )
            
            if st.button("Submit Answer"):
                if answer == question['correct_answer']:
                    st.session_state.quiz_score += 1
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. Correct answer: {chr(65 + question['correct_answer'])}")
                
                st.info(f"Explanation: {question['explanation']}")
                st.session_state.quiz_index += 1
                
                if st.session_state.quiz_index >= len(quiz):
                    # Quiz completed
                    score = st.session_state.quiz_score
                    total = len(quiz)
                    percentage = (score / total) * 100
                    
                    st.balloons()
                    st.markdown(f"## Quiz Completed!")
                    st.metric("Your Score", f"{score}/{total} ({percentage:.1f}%)")
                    
                    # Update user data
                    st.session_state.user_data['quiz_scores'].append(percentage)
                    st.session_state.user_data['total_points'] += score * 10
                    
                    if st.button("Take Another Quiz"):
                        del st.session_state.current_quiz
                        del st.session_state.quiz_index
                        del st.session_state.quiz_score
                        st.rerun()
                else:
                    st.rerun()

elif selected in ["Status", "स्थिति"]:
    if st.session_state.language == 'hi':
        status_title = "एप्लिकेशन स्थिति"
    else:
        status_title = "Application Status"
    
    st.markdown(f"## 📊 {status_title}")
    
    st.success("✅ Streamlit: Working")
    st.success("✅ Basic functionality: Working")
    st.success("✅ Language switching: Working")
    
    if openai_available:
        st.success("✅ OpenAI package: Available")
        if "OPENAI_API_KEY" in os.environ:
            st.success("✅ OpenAI API key: Configured")
        else:
            st.warning("⚠️ OpenAI API key: Not configured")
    else:
        st.error("❌ OpenAI package: Not available")
    
    if menu_available:
        st.success("✅ Menu navigation: Available")
    else:
        st.warning("⚠️ Menu navigation: Using basic selectbox")

st.markdown("---")
st.markdown("Built for Indian government job preparation | भारतीय सरकारी नौकरी तैयारी के लिए निर्मित")
