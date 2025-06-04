import streamlit as st
from streamlit_option_menu import option_menu
import os
from utils.language_manager import LanguageManager
from utils.data_manager import DataManager
from modules import quiz, study_plan, analytics, mock_interview, current_affairs

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

# Page configuration
st.set_page_config(
    page_title="AI Government Job Prep | भारत सरकारी नौकरी तैयारी",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PWA Meta tags and manifest
st.markdown("""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#FF9933">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="AI Gov Prep">
    <link rel="manifest" href="/static/manifest.json">
    <link rel="apple-touch-icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='33.33' fill='%23FF9933'/%3E%3Crect y='33.33' width='100' height='33.33' fill='%23FFFFFF'/%3E%3Crect y='66.66' width='100' height='33.33' fill='%23138808'/%3E%3Ccircle cx='50' cy='50' r='10' fill='%23000080'/%3E%3C/svg%3E">
</head>
<script>
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/static/sw.js');
        });
    }
</script>
""", unsafe_allow_html=True)

# Initialize managers
lang_manager = LanguageManager()
data_manager = DataManager()

# Custom CSS for Indian flag theme
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
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF9933;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .achievement-badge {
        background: linear-gradient(45deg, #FF9933, #138808);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .sidebar .stSelectbox > div > div {
        background-color: #F0F2F6;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Language toggle in sidebar
    with st.sidebar:
        st.markdown("### 🌐 Language / भाषा")
        language = st.selectbox(
            "Choose Language",
            options=['en', 'hi'],
            format_func=lambda x: "English" if x == 'en' else "हिंदी",
            key="language_selector"
        )
        
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()

    # Main header
    header_text = lang_manager.get_text('app_title', st.session_state.language)
    st.markdown(f'<div class="main-header"><h1>🇮🇳 {header_text}</h1></div>', unsafe_allow_html=True)
    
    # Navigation menu
    menu_options = lang_manager.get_menu_options(st.session_state.language)
    
    selected = option_menu(
        menu_title=None,
        options=list(menu_options.keys()),
        icons=["house-fill", "question-circle-fill", "calendar-check-fill", 
               "graph-up", "mic-fill", "newspaper"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#FF9933", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#138808"},
        }
    )
    
    # Route to appropriate page
    if selected == list(menu_options.keys())[0]:  # Home
        show_home_page()
    elif selected == list(menu_options.keys())[1]:  # Quiz
        quiz.show_quiz_page(st.session_state.language, lang_manager)
    elif selected == list(menu_options.keys())[2]:  # Study Plan
        study_plan.show_study_plan_page(st.session_state.language, lang_manager)
    elif selected == list(menu_options.keys())[3]:  # Analytics
        analytics.show_analytics_page(st.session_state.language, lang_manager)
    elif selected == list(menu_options.keys())[4]:  # Mock Interview
        mock_interview.show_mock_interview_page(st.session_state.language, lang_manager)
    elif selected == list(menu_options.keys())[5]:  # Current Affairs
        current_affairs.show_current_affairs_page(st.session_state.language, lang_manager)

def show_home_page():
    """Display the home page with welcome message and user setup"""
    lang = st.session_state.language
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## {lang_manager.get_text('welcome_message', lang)}")
        st.markdown(lang_manager.get_text('app_description', lang))
        
        # User profile setup
        with st.expander(lang_manager.get_text('profile_setup', lang), expanded=not st.session_state.user_data['name']):
            name = st.text_input(
                lang_manager.get_text('your_name', lang),
                value=st.session_state.user_data['name']
            )
            
            exam_types = lang_manager.get_exam_types(lang)
            exam_type = st.selectbox(
                lang_manager.get_text('target_exam', lang),
                options=list(exam_types.keys()),
                index=0 if not st.session_state.user_data['exam_type'] else list(exam_types.keys()).index(st.session_state.user_data['exam_type'])
            )
            
            target_date = st.date_input(lang_manager.get_text('target_date', lang))
            
            study_hours = st.slider(
                lang_manager.get_text('daily_study_hours', lang),
                min_value=1,
                max_value=12,
                value=st.session_state.user_data['study_hours_per_day']
            )
            
            if st.button(lang_manager.get_text('save_profile', lang)):
                st.session_state.user_data.update({
                    'name': name,
                    'exam_type': exam_type,
                    'target_date': target_date,
                    'study_hours_per_day': study_hours
                })
                st.success(lang_manager.get_text('profile_saved', lang))
                st.rerun()
    
    with col2:
        # Quick stats
        if st.session_state.user_data['name']:
            st.markdown(f"### {lang_manager.get_text('quick_stats', lang)}")
            
            # Total points
            st.metric(
                lang_manager.get_text('total_points', lang),
                st.session_state.user_data['total_points'],
                delta=None
            )
            
            # Study streak
            st.metric(
                lang_manager.get_text('study_streak', lang),
                f"{st.session_state.user_data['study_streaks']} {lang_manager.get_text('days', lang)}",
                delta=None
            )
            
            # Quizzes completed
            st.metric(
                lang_manager.get_text('quizzes_completed', lang),
                len(st.session_state.user_data['quiz_scores']),
                delta=None
            )
            
            # Achievements
            if st.session_state.user_data['badges']:
                st.markdown(f"### {lang_manager.get_text('achievements', lang)}")
                for badge in st.session_state.user_data['badges']:
                    st.markdown(f'<div class="achievement-badge">{badge}</div>', unsafe_allow_html=True)

    # Quick actions
    st.markdown(f"### {lang_manager.get_text('quick_actions', lang)}")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(f"📝 {lang_manager.get_text('take_quiz', lang)}", use_container_width=True):
            st.session_state.page = 'Quiz'
            st.rerun()
    
    with col2:
        if st.button(f"📊 {lang_manager.get_text('view_progress', lang)}", use_container_width=True):
            st.session_state.page = 'Analytics'
            st.rerun()
    
    with col3:
        if st.button(f"🎯 {lang_manager.get_text('study_plan', lang)}", use_container_width=True):
            st.session_state.page = 'Study Plan'
            st.rerun()
    
    with col4:
        if st.button(f"🎙️ {lang_manager.get_text('mock_interview', lang)}", use_container_width=True):
            st.session_state.page = 'Mock Interview'
            st.rerun()

if __name__ == "__main__":
    main()
