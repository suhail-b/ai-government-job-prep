import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="AI Government Job Prep | भारत सरकारी नौकरी तैयारी",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check for OpenAI API key
if "OPENAI_API_KEY" not in os.environ:
    st.error("OpenAI API key not found. Please add OPENAI_API_KEY to your app secrets.")
    st.stop()

# Try to import required packages
try:
    from streamlit_option_menu import option_menu
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    from openai import OpenAI
    import json
    from datetime import datetime, timedelta
    import time
    import requests
except ImportError as e:
    st.error(f"Missing required package: {e}")
    st.info("Please ensure all required packages are installed.")
    st.stop()

# Initialize OpenAI client
try:
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")
    st.stop()

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.language = 'en'
    st.session_state.user_data = {
        'name': '',
        'exam_type': '',
        'target_date': None,
        'study_hours_per_day': 2,
        'quiz_scores': [],
        'study_streaks': 0,
        'badges': [],
        'total_points': 0
    }
    st.session_state.quiz_history = []

# Language translations
translations = {
    'en': {
        'app_title': 'AI Government Job Prep',
        'welcome_message': 'Welcome to AI-Powered Government Job Preparation',
        'app_description': '🎯 Prepare for Indian government exams with AI-powered quizzes, personalized study plans, and comprehensive analytics.',
        'home': 'Home',
        'quiz': 'AI Quiz',
        'study_plan': 'Study Plan',
        'analytics': 'Analytics',
        'mock_interview': 'Mock Interview',
        'current_affairs': 'Current Affairs',
        'profile_setup': 'Profile Setup',
        'your_name': 'Your Name',
        'target_exam': 'Target Exam',
        'save_profile': 'Save Profile',
        'profile_saved': 'Profile saved successfully!',
        'take_quiz': 'Take Quiz',
        'generate_quiz': 'Generate Quiz',
        'select_topic': 'Select Topic',
        'select_difficulty': 'Select Difficulty',
        'submit_answer': 'Submit Answer',
        'quiz_completed': 'Quiz Completed!',
        'your_score': 'Your Score',
        'points_earned': 'Points Earned'
    },
    'hi': {
        'app_title': 'एआई सरकारी नौकरी तैयारी',
        'welcome_message': 'एआई-संचालित सरकारी नौकरी तैयारी में आपका स्वागत है',
        'app_description': '🎯 एआई-संचालित क्विज़, व्यक्तिगत अध्ययन योजना और व्यापक विश्लेषण के साथ भारतीय सरकारी परीक्षाओं की तैयारी करें।',
        'home': 'होम',
        'quiz': 'एआई क्विज़',
        'study_plan': 'अध्ययन योजना',
        'analytics': 'विश्लेषण',
        'mock_interview': 'मॉक इंटरव्यू',
        'current_affairs': 'समसामयिकी',
        'profile_setup': 'प्रोफाइल सेटअप',
        'your_name': 'आपका नाम',
        'target_exam': 'लक्षित परीक्षा',
        'save_profile': 'प्रोफाइल सेव करें',
        'profile_saved': 'प्रोफाइल सफलतापूर्वक सेव हो गया!',
        'take_quiz': 'क्विज़ लें',
        'generate_quiz': 'क्विज़ जेनरेट करें',
        'select_topic': 'विषय चुनें',
        'select_difficulty': 'कठिनाई चुनें',
        'submit_answer': 'उत्तर सबमिट करें',
        'quiz_completed': 'क्विज़ पूर्ण!',
        'your_score': 'आपका स्कोर',
        'points_earned': 'अर्जित अंक'
    }
}

def get_text(key, language='en'):
    return translations.get(language, {}).get(key, key)

# CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%);
        padding: 1rem;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: #262730;
        font-weight: bold;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background: linear-gradient(45deg, #FF9933, #138808);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

def generate_quiz_questions(topic, difficulty, language='en', num_questions=5):
    """Generate quiz questions using OpenAI"""
    try:
        lang_instruction = "in Hindi (Devanagari script)" if language == 'hi' else "in English"
        
        prompt = f"""Generate {num_questions} multiple choice questions for Indian government job preparation exams 
        on the topic "{topic}" with difficulty level {difficulty}/5 {lang_instruction}.
        
        Return the response as a JSON object with this structure:
        {{
            "questions": [
                {{
                    "question": "Question text here",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 0,
                    "explanation": "Detailed explanation"
                }}
            ]
        }}
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in Indian government job preparation."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("questions", [])
        
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return []

def show_home_page():
    """Display home page"""
    lang = st.session_state.language
    
    st.markdown(f"## {get_text('welcome_message', lang)}")
    st.markdown(get_text('app_description', lang))
    
    # Profile setup
    with st.expander(get_text('profile_setup', lang), expanded=not st.session_state.user_data['name']):
        name = st.text_input(get_text('your_name', lang), value=st.session_state.user_data['name'])
        
        exam_types = {
            'UPSC Civil Services': 'UPSC Civil Services',
            'SSC CGL': 'SSC Combined Graduate Level',
            'Banking': 'Banking Exams',
            'Railway': 'Railway Recruitment',
            'Other': 'Other'
        }
        
        exam_type = st.selectbox(get_text('target_exam', lang), options=list(exam_types.keys()))
        
        if st.button(get_text('save_profile', lang)):
            st.session_state.user_data.update({
                'name': name,
                'exam_type': exam_type
            })
            st.success(get_text('profile_saved', lang))
            st.rerun()
    
    # Quick action
    if st.button(f"📝 {get_text('take_quiz', lang)}", use_container_width=True):
        st.session_state.current_page = 'quiz'
        st.rerun()

def show_quiz_page():
    """Display quiz page"""
    lang = st.session_state.language
    
    st.markdown(f"## 📝 AI Quiz Generator")
    
    # Quiz configuration
    topics = {
        'General Knowledge': 'सामान्य ज्ञान' if lang == 'hi' else 'General Knowledge',
        'Indian History': 'भारतीय इतिहास' if lang == 'hi' else 'Indian History',
        'Geography': 'भूगोल' if lang == 'hi' else 'Geography',
        'Current Affairs': 'समसामयिकी' if lang == 'hi' else 'Current Affairs'
    }
    
    selected_topic = st.selectbox(get_text('select_topic', lang), options=list(topics.keys()))
    difficulty = st.slider(get_text('select_difficulty', lang), min_value=1, max_value=5, value=3)
    
    if st.button(f"🚀 {get_text('generate_quiz', lang)}", use_container_width=True):
        with st.spinner("Generating questions..."):
            questions = generate_quiz_questions(selected_topic, difficulty, lang, 5)
        
        if questions:
            st.session_state.current_quiz = {
                'questions': questions,
                'current_question': 0,
                'answers': [],
                'score': 0
            }
            st.rerun()
    
    # Display quiz if active
    if 'current_quiz' in st.session_state:
        quiz = st.session_state.current_quiz
        current_q = quiz['current_question']
        
        if current_q < len(quiz['questions']):
            question = quiz['questions'][current_q]
            
            st.markdown(f"### Question {current_q + 1}/{len(quiz['questions'])}")
            st.markdown(f"**{question['question']}**")
            
            user_answer = st.radio(
                "Select your answer:",
                options=range(len(question['options'])),
                format_func=lambda x: f"{chr(65+x)}. {question['options'][x]}"
            )
            
            if st.button(get_text('submit_answer', lang)):
                is_correct = user_answer == question['correct_answer']
                if is_correct:
                    quiz['score'] += 1
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Incorrect!")
                
                quiz['current_question'] += 1
                time.sleep(2)
                st.rerun()
        else:
            # Quiz completed
            score = quiz['score']
            total = len(quiz['questions'])
            percentage = (score / total) * 100
            
            st.markdown(f"# 🎉 {get_text('quiz_completed', lang)}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(get_text('your_score', lang), f"{score}/{total}")
            with col2:
                st.metric("Percentage", f"{percentage:.1f}%")
            with col3:
                points = score * 10
                st.metric(get_text('points_earned', lang), points)
            
            # Update user data
            st.session_state.user_data['total_points'] += points
            st.session_state.user_data['quiz_scores'].append(percentage)
            
            if st.button("🔄 Take Another Quiz"):
                del st.session_state.current_quiz
                st.rerun()

def main():
    # Language selector in sidebar
    with st.sidebar:
        st.markdown("### 🌐 Language / भाषा")
        language = st.selectbox(
            "Choose Language",
            options=['en', 'hi'],
            format_func=lambda x: "English" if x == 'en' else "हिंदी"
        )
        
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()
    
    # Main header
    header_text = get_text('app_title', st.session_state.language)
    st.markdown(f'<div class="main-header"><h1>🇮🇳 {header_text}</h1></div>', unsafe_allow_html=True)
    
    # Navigation
    menu_options = {
        get_text('home', st.session_state.language): 'home',
        get_text('quiz', st.session_state.language): 'quiz'
    }
    
    selected = option_menu(
        menu_title=None,
        options=list(menu_options.keys()),
        icons=["house-fill", "question-circle-fill"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#FF9933", "font-size": "20px"},
            "nav-link-selected": {"background-color": "#138808"},
        }
    )
    
    # Route to pages
    if selected == list(menu_options.keys())[0]:  # Home
        show_home_page()
    elif selected == list(menu_options.keys())[1]:  # Quiz
        show_quiz_page()

if __name__ == "__main__":
    main()
