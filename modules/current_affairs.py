import streamlit as st
from utils.ai_services import AIServices
from utils.data_manager import DataManager
from utils.language_manager import LanguageManager
from datetime import datetime, timedelta
import requests
import json

def show_current_affairs_page(language: str, lang_manager: LanguageManager):
    """Display the current affairs tracker page"""
    
    ai_services = AIServices()
    data_manager = DataManager()
    
    st.markdown(f"## 📰 {lang_manager.get_text('current_affairs_tracker', language)}")
    
    # Current affairs categories
    categories = lang_manager.get_current_affairs_categories(language)
    
    # Tab layout for different sections
    tab1, tab2, tab3 = st.tabs([
        "Latest Updates" if language == 'en' else "नवीनतम अपडेट",
        "Practice Questions" if language == 'en' else "अभ्यास प्रश्न",
        "My Progress" if language == 'en' else "मेरी प्रगति"
    ])
    
    with tab1:
        display_latest_updates(categories, language, lang_manager)
    
    with tab2:
        display_practice_questions(categories, language, ai_services, data_manager, lang_manager)
    
    with tab3:
        display_current_affairs_progress(data_manager, language, lang_manager)

def display_latest_updates(categories: dict, language: str, lang_manager: LanguageManager):
    """Display latest current affairs updates"""
    
    st.markdown(f"### 🌟 {lang_manager.get_text('latest_updates', language)}")
    
    # Category filter
    selected_category = st.selectbox(
        "Select Category" if language == 'en' else "श्रेणी चुनें",
        options=list(categories.keys()),
        key="ca_category_filter"
    )
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "From Date" if language == 'en' else "दिनांक से",
            value=datetime.now().date() - timedelta(days=7),
            key="ca_start_date"
        )
    
    with col2:
        end_date = st.date_input(
            "To Date" if language == 'en' else "दिनांक तक",
            value=datetime.now().date(),
            key="ca_end_date"
        )
    
    # Refresh button
    if st.button("🔄 Refresh Updates" if language == 'en' else "🔄 अपडेट रीफ्रेश करें"):
        with st.spinner("Fetching latest updates..." if language == 'en' else "नवीनतम अपडेट प्राप्त कर रहे हैं..."):
            updates = fetch_current_affairs_updates(selected_category, start_date, end_date, language)
            display_news_updates(updates, language)
    
    # Display sample/cached updates when API is not available
    st.markdown("---")
    st.markdown("#### 📋 Recent Important Updates" if language == 'en' else "#### 📋 हाल के महत्वपूर्ण अपडेट")
    
    # Note: In a real implementation, this would fetch from news APIs
    st.info("Note: Connect news APIs for live updates. Currently showing educational framework." if language == 'en'
           else "नोट: लाइव अपडेट के लिए न्यूज API कनेक्ट करें। वर्तमान में शैक्षणिक ढांचा दिखाया जा रहा है।")
    
    # Educational framework for current affairs structure
    display_current_affairs_framework(selected_category, language)

def display_practice_questions(categories: dict, language: str, ai_services: AIServices, 
                             data_manager: DataManager, lang_manager: LanguageManager):
    """Display current affairs practice questions"""
    
    st.markdown(f"### 📝 {lang_manager.get_text('generate_questions', language)}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Topic selection
        selected_category = st.selectbox(
            lang_manager.get_text('news_topic', language),
            options=list(categories.keys()),
            key="ca_question_category"
        )
        
        # Specific topic input
        specific_topic = st.text_input(
            "Specific Topic (Optional)" if language == 'en' else "विशिष्ट विषय (वैकल्पिक)",
            placeholder="e.g., Budget 2024, G20 Summit" if language == 'en' else "जैसे, बजट 2024, जी20 शिखर सम्मेलन",
            key="ca_specific_topic"
        )
        
        # Number of questions
        num_questions = st.selectbox(
            "Number of Questions" if language == 'en' else "प्रश्नों की संख्या",
            options=[3, 5, 10],
            index=1,
            key="ca_num_questions"
        )
    
    with col2:
        # Time period selection
        time_period = st.selectbox(
            "Time Period" if language == 'en' else "समय अवधि",
            options=[
                "Last 30 days" if language == 'en' else "पिछले 30 दिन",
                "Last 3 months" if language == 'en' else "पिछले 3 महीने",
                "Last 6 months" if language == 'en' else "पिछले 6 महीने",
                "Current Year" if language == 'en' else "वर्तमान वर्ष"
            ],
            key="ca_time_period"
        )
        
        # Difficulty level
        difficulty = st.slider(
            "Difficulty Level" if language == 'en' else "कठिनाई स्तर",
            min_value=1,
            max_value=5,
            value=3,
            key="ca_difficulty"
        )
    
    # Generate questions button
    if st.button(f"🚀 {lang_manager.get_text('generate_questions', language)}", use_container_width=True):
        generate_current_affairs_quiz(selected_category, specific_topic, num_questions, difficulty, 
                                    language, ai_services, data_manager, lang_manager)

def generate_current_affairs_quiz(category: str, specific_topic: str, num_questions: int, 
                                difficulty: int, language: str, ai_services: AIServices,
                                data_manager: DataManager, lang_manager: LanguageManager):
    """Generate and display current affairs quiz"""
    
    # Prepare topic for AI
    topic_for_ai = f"{category}"
    if specific_topic:
        topic_for_ai += f" - {specific_topic}"
    
    with st.spinner(lang_manager.get_text('loading', language)):
        questions = ai_services.generate_current_affairs_questions(topic_for_ai, language)
    
    if not questions:
        st.error("Unable to generate current affairs questions. Please check your OpenAI API key or try again later." 
                if language == 'en' else "समसामयिकी प्रश्न जेनरेट करने में असमर्थ। कृपया अपनी OpenAI API key जांचें या बाद में पुनः प्रयास करें।")
        return
    
    # Limit to requested number
    questions = questions[:num_questions]
    
    # Initialize quiz session for current affairs
    if 'ca_quiz_session' not in st.session_state:
        st.session_state.ca_quiz_session = {
            'questions': questions,
            'current_question': 0,
            'answers': [],
            'score': 0,
            'category': category,
            'language': language
        }
    
    # Display current affairs quiz
    display_ca_quiz(st.session_state.ca_quiz_session, data_manager, lang_manager)

def display_ca_quiz(session: dict, data_manager: DataManager, lang_manager: LanguageManager):
    """Display current affairs quiz interface"""
    
    language = session['language']
    current_q_idx = session['current_question']
    
    if current_q_idx < len(session['questions']):
        question = session['questions'][current_q_idx]
        
        # Progress bar
        progress = (current_q_idx + 1) / len(session['questions'])
        st.progress(progress)
        st.markdown(f"**Current Affairs Quiz {current_q_idx + 1}/{len(session['questions'])}**")
        
        # Question display
        st.markdown(f"### 📰 {question['question']}")
        
        # Date relevance if available
        if question.get('date_relevance'):
            st.caption(f"**Relevant Time Period:** {question['date_relevance']}")
        
        # Answer options
        user_answer = st.radio(
            "Select your answer:",
            options=range(len(question['options'])),
            format_func=lambda x: f"{chr(65+x)}. {question['options'][x]}",
            key=f"ca_question_{current_q_idx}"
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button(lang_manager.get_text('submit_answer', language), use_container_width=True):
                # Record answer
                is_correct = user_answer == question['correct_answer']
                session['answers'].append({
                    'question_idx': current_q_idx,
                    'user_answer': user_answer,
                    'correct_answer': question['correct_answer'],
                    'is_correct': is_correct,
                    'question_text': question['question'],
                    'explanation': question.get('explanation', '')
                })
                
                if is_correct:
                    session['score'] += 1
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Incorrect!")
                    st.markdown(f"**{lang_manager.get_text('correct_answer', language)}:** {chr(65 + question['correct_answer'])}. {question['options'][question['correct_answer']]}")
                
                if question.get('explanation'):
                    st.info(f"**{lang_manager.get_text('explanation', language)}:** {question['explanation']}")
                
                # Move to next question
                session['current_question'] += 1
                
                import time
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("⏭️ Skip"):
                session['answers'].append({
                    'question_idx': current_q_idx,
                    'user_answer': -1,
                    'correct_answer': question['correct_answer'],
                    'is_correct': False,
                    'question_text': question['question'],
                    'explanation': question.get('explanation', '')
                })
                session['current_question'] += 1
                st.rerun()
    
    else:
        # Quiz completed
        display_ca_quiz_results(session, data_manager, lang_manager)

def display_ca_quiz_results(session: dict, data_manager: DataManager, lang_manager: LanguageManager):
    """Display current affairs quiz results"""
    
    language = session['language']
    score = session['score']
    total = len(session['questions'])
    percentage = (score / total) * 100 if total > 0 else 0
    
    st.markdown(f"# 🎉 Current Affairs Quiz Completed!" if language == 'en' else "# 🎉 समसामयिकी क्विज़ पूर्ण!")
    
    # Performance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Score" if language == 'en' else "स्कोर", f"{score}/{total}")
    
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    
    with col3:
        points_earned = score * 10  # 10 points per correct answer
        st.metric("Points Earned" if language == 'en' else "अर्जित अंक", points_earned)
    
    # Update user progress
    if 'current_affairs_score' not in st.session_state.user_data:
        st.session_state.user_data['current_affairs_score'] = 0
    
    st.session_state.user_data['current_affairs_score'] += points_earned
    st.session_state.user_data['total_points'] += points_earned
    
    # Performance feedback
    if percentage >= 80:
        st.success("🌟 Excellent! You're well-informed about current affairs!" if language == 'en'
                  else "🌟 उत्कृष्ट! आप समसामयिकी के बारे में अच्छी जानकारी रखते हैं!")
    elif percentage >= 60:
        st.info("👍 Good performance! Keep reading news regularly." if language == 'en'
               else "👍 अच्छा प्रदर्शन! नियमित रूप से समाचार पढ़ते रहें।")
    else:
        st.warning("📚 Need to focus more on current affairs. Read newspapers daily!" if language == 'en'
                  else "📚 समसामयिकी पर अधिक ध्यान देने की आवश्यकता है। दैनिक समाचारपत्र पढ़ें!")
    
    # Detailed review
    with st.expander("📋 Detailed Review" if language == 'en' else "📋 विस्तृत समीक्षा"):
        for i, answer in enumerate(session['answers']):
            question = session['questions'][answer['question_idx']]
            
            if answer['is_correct']:
                st.success(f"**Q{i+1}.** {answer['question_text']}")
            else:
                st.error(f"**Q{i+1}.** {answer['question_text']}")
                if answer['user_answer'] != -1:
                    st.markdown(f"Your answer: ❌ {question['options'][answer['user_answer']]}")
                else:
                    st.markdown("Your answer: ⏭️ Skipped")
                st.markdown(f"Correct answer: ✅ {question['options'][answer['correct_answer']]}")
            
            if answer['explanation']:
                st.info(f"💡 {answer['explanation']}")
            
            st.divider()
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Another Quiz" if language == 'en' else "🔄 दूसरी क्विज़", use_container_width=True):
            if 'ca_quiz_session' in st.session_state:
                del st.session_state.ca_quiz_session
            st.rerun()
    
    with col2:
        if st.button("📊 View Progress" if language == 'en' else "📊 प्रगति देखें", use_container_width=True):
            st.session_state.page = 'Analytics'
            st.rerun()
    
    with col3:
        if st.button("🏠 Home" if language == 'en' else "🏠 होम", use_container_width=True):
            if 'ca_quiz_session' in st.session_state:
                del st.session_state.ca_quiz_session
            st.session_state.page = 'Home'
            st.rerun()

def display_current_affairs_progress(data_manager: DataManager, language: str, lang_manager: LanguageManager):
    """Display user's current affairs progress and statistics"""
    
    st.markdown(f"### 📈 Current Affairs Performance" if language == 'en' else "### 📈 समसामयिकी प्रदर्शन")
    
    # Get current affairs specific stats
    ca_score = st.session_state.user_data.get('current_affairs_score', 0)
    
    # Progress metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "CA Points Earned" if language == 'en' else "समसामयिकी अंक",
            ca_score
        )
    
    with col2:
        # Calculate reading streak (simplified)
        reading_streak = calculate_reading_streak()
        st.metric(
            "Reading Streak" if language == 'en' else "पठन श्रृंखला",
            f"{reading_streak} days" if language == 'en' else f"{reading_streak} दिन"
        )
    
    with col3:
        topics_covered = len(set([quiz.get('topic', '') for quiz in data_manager.get_quiz_history() 
                                if 'Current Affairs' in quiz.get('topic', '')]))
        st.metric(
            "Topics Covered" if language == 'en' else "कवर किए गए विषय",
            topics_covered
        )
    
    # Current affairs recommendations
    st.markdown("---")
    st.markdown("### 💡 Study Recommendations" if language == 'en' else "### 💡 अध्ययन सुझाव")
    
    recommendations = get_current_affairs_recommendations(language, ca_score)
    for rec in recommendations:
        st.info(f"📌 {rec}")
    
    # Important topics to focus on
    st.markdown("### 🎯 Important Topics to Focus" if language == 'en' else "### 🎯 महत्वपूर्ण विषय")
    
    important_topics = get_important_current_affairs_topics(language)
    
    cols = st.columns(2)
    for i, topic in enumerate(important_topics):
        with cols[i % 2]:
            st.markdown(f"🔸 {topic}")

def fetch_current_affairs_updates(category: str, start_date, end_date, language: str):
    """Fetch current affairs updates from news sources"""
    
    # Note: In a real implementation, this would integrate with news APIs like:
    # - NewsAPI
    # - Hindu API
    # - PIB (Press Information Bureau) RSS feeds
    # - Government websites RSS
    
    # For now, return empty list as we don't want to mock data
    return []

def display_news_updates(updates: list, language: str):
    """Display fetched news updates"""
    
    if not updates:
        st.info("No updates available. Please check your internet connection or try again later." 
               if language == 'en' else "कोई अपडेट उपलब्ध नहीं है। कृपया अपना इंटरनेट कनेक्शन जांचें या बाद में पुनः प्रयास करें।")
        return
    
    for update in updates:
        with st.container():
            st.markdown(f"### {update.get('title', '')}")
            st.markdown(f"**Date:** {update.get('date', '')}")
            st.markdown(update.get('summary', ''))
            if update.get('source'):
                st.caption(f"Source: {update['source']}")
            st.divider()

def display_current_affairs_framework(category: str, language: str):
    """Display educational framework for current affairs structure"""
    
    st.markdown("#### 📚 Study Framework" if language == 'en' else "#### 📚 अध्ययन ढांचा")
    
    frameworks = {
        'en': {
            'National Politics': [
                "Parliament sessions and important bills",
                "Government policies and schemes",
                "Election updates and political developments",
                "Constitutional amendments and judicial decisions"
            ],
            'International Relations': [
                "Bilateral and multilateral agreements",
                "International summits and conferences",
                "Trade relations and economic partnerships",
                "Global conflicts and peace initiatives"
            ],
            'Economy & Business': [
                "Budget announcements and fiscal policies",
                "Economic indicators and market trends",
                "Banking and financial sector updates",
                "Industry developments and corporate news"
            ],
            'Science & Technology': [
                "Space missions and scientific achievements",
                "Technology innovations and digital initiatives",
                "Healthcare breakthroughs and medical research",
                "Environmental technology and climate solutions"
            ]
        },
        'hi': {
            'National Politics': [
                "संसद सत्र और महत्वपूर्ण विधेयक",
                "सरकारी नीतियां और योजनाएं",
                "चुनाव अपडेट और राजनीतिक विकास",
                "संवैधानिक संशोधन और न्यायिक निर्णय"
            ],
            'International Relations': [
                "द्विपक्षीय और बहुपक्षीय समझौते",
                "अंतर्राष्ट्रीय शिखर सम्मेलन और सम्मेलन",
                "व्यापारिक संबंध और आर्थिक साझेदारी",
                "वैश्विक संघर्ष और शांति पहल"
            ],
            'Economy & Business': [
                "बजट घोषणाएं और राजकोषीय नीतियां",
                "आर्थिक संकेतक और बाजार रुझान",
                "बैंकिंग और वित्तीय क्षेत्र अपडेट",
                "उद्योग विकास और कॉर्पोरेट समाचार"
            ],
            'Science & Technology': [
                "अंतरिक्ष मिशन और वैज्ञानिक उपलब्धियां",
                "प्रौद्योगिकी नवाचार और डिजिटल पहल",
                "स्वास्थ्य सेवा में सफलताएं और चिकित्सा अनुसंधान",
                "पर्यावरण प्रौद्योगिकी और जलवायु समाधान"
            ]
        }
    }
    
    lang_key = 'hi' if language == 'hi' else 'en'
    framework_items = frameworks.get(lang_key, {}).get(category, frameworks[lang_key]['National Politics'])
    
    for item in framework_items:
        st.markdown(f"• {item}")

def calculate_reading_streak():
    """Calculate user's reading streak (simplified implementation)"""
    # In a real implementation, this would track daily reading activity
    # For now, return a placeholder value
    return 1

def get_current_affairs_recommendations(language: str, ca_score: int) -> list:
    """Get personalized current affairs study recommendations"""
    
    if language == 'hi':
        if ca_score < 50:
            return [
                "दैनिक समाचारपत्र पढ़ने की आदत बनाएं",
                "सरकारी वेबसाइटों से नवीनतम योजनाओं की जानकारी लें",
                "मासिक करंट अफेयर्स पत्रिकाओं का अध्ययन करें",
                "समसामयिकी के लिए विश्वसनीय YouTube चैनल फॉलो करें"
            ]
        else:
            return [
                "अंतर्राष्ट्रीय समाचारों पर अधिक ध्यान दें",
                "आर्थिक सर्वेक्षण और बजट दस्तावेजों का अध्ययन करें",
                "समसामयिकी के प्रश्नों का नियमित अभ्यास करें",
                "समूह चर्चा में भाग लेकर अपनी समझ बढ़ाएं"
            ]
    else:
        if ca_score < 50:
            return [
                "Develop a habit of reading daily newspapers",
                "Follow reliable news websites and apps",
                "Study monthly current affairs magazines",
                "Subscribe to government press releases and PIB updates"
            ]
        else:
            return [
                "Focus more on international affairs and global events",
                "Read economic surveys and budget documents",
                "Practice current affairs MCQs regularly",
                "Participate in group discussions to enhance understanding"
            ]

def get_important_current_affairs_topics(language: str) -> list:
    """Get list of important current affairs topics"""
    
    if language == 'hi':
        return [
            "भारत की G20 अध्यक्षता",
            "डिजिटल इंडिया पहल",
            "आत्मनिर्भर भारत अभियान",
            "जलवायु परिवर्तन और COP28",
            "भारत-चीन सीमा विवाद",
            "कृषि सुधार और MSP",
            "स्वच्छ भारत मिशन",
            "नई शिक्षा नीति 2020",
            "COVID-19 और वैक्सीनेशन",
            "अंतरिक्ष मिशन (चंद्रयान, मंगलयान)"
        ]
    else:
        return [
            "India's G20 Presidency",
            "Digital India Initiative",
            "Atmanirbhar Bharat Campaign",
            "Climate Change and COP28",
            "India-China Border Issues",
            "Agricultural Reforms and MSP",
            "Swachh Bharat Mission",
            "New Education Policy 2020",
            "COVID-19 and Vaccination Drive",
            "Space Missions (Chandrayaan, Mangalyaan)"
        ]
