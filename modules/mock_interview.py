import streamlit as st
from utils.ai_services import AIServices
from utils.data_manager import DataManager
from utils.language_manager import LanguageManager
import time
from datetime import datetime

def show_mock_interview_page(language: str, lang_manager: LanguageManager):
    """Display the AI mock interview page"""
    
    ai_services = AIServices()
    data_manager = DataManager()
    
    st.markdown(f"## 🎙️ {lang_manager.get_text('ai_mock_interview', language)}")
    
    # Interview setup
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Interview Preparation" if language == 'en' else "### 🎯 साक्षात्कार तैयारी")
        
        # Topic selection
        interview_topics = lang_manager.get_interview_topics(language)
        selected_topic = st.selectbox(
            lang_manager.get_text('interview_topic', language),
            options=list(interview_topics.keys()),
            key="interview_topic"
        )
        
        # Interview type
        interview_types = {
            'Personal Interview': 'व्यक्तिगत साक्षात्कार' if language == 'hi' else 'Personal Interview',
            'Technical Interview': 'तकनीकी साक्षात्कार' if language == 'hi' else 'Technical Interview',
            'Group Discussion': 'समूह चर्चा' if language == 'hi' else 'Group Discussion',
            'Stress Interview': 'तनाव साक्षात्कार' if language == 'hi' else 'Stress Interview'
        }
        
        interview_type = st.selectbox(
            "Interview Type" if language == 'en' else "साक्षात्कार प्रकार",
            options=list(interview_types.keys()),
            format_func=lambda x: interview_types[x]
        )
        
        # Difficulty level
        difficulty = st.slider(
            "Interview Difficulty" if language == 'en' else "साक्षात्कार कठिनाई",
            min_value=1,
            max_value=5,
            value=3
        )
    
    with col2:
        # Interview tips
        st.markdown("### 💡 Interview Tips" if language == 'en' else "### 💡 साक्षात्कार सुझाव")
        
        tips = get_interview_tips(language)
        for tip in tips[:5]:
            st.markdown(f"• {tip}")
        
        # Recent interview scores
        if st.session_state.user_data.get('interview_scores'):
            recent_scores = st.session_state.user_data['interview_scores'][-3:]
            st.markdown("### 📊 Recent Scores" if language == 'en' else "### 📊 हाल के स्कोर")
            for score in recent_scores:
                st.metric("Score", f"{score['score']}/100")
    
    # Start interview button
    if st.button(f"🚀 {lang_manager.get_text('start_interview', language)}", use_container_width=True):
        start_interview_session(selected_topic, interview_type, difficulty, language, ai_services, lang_manager)

def start_interview_session(topic: str, interview_type: str, difficulty: int, language: str, 
                           ai_services: AIServices, lang_manager: LanguageManager):
    """Start an interview session"""
    
    # Initialize interview session
    if 'interview_session' not in st.session_state:
        st.session_state.interview_session = {
            'topic': topic,
            'type': interview_type,
            'difficulty': difficulty,
            'language': language,
            'questions': generate_interview_questions(topic, interview_type, difficulty, language),
            'current_question': 0,
            'responses': [],
            'start_time': time.time()
        }
    
    session = st.session_state.interview_session
    
    if session['current_question'] < len(session['questions']):
        display_interview_question(session, ai_services, lang_manager)
    else:
        display_interview_results(session, lang_manager)

def generate_interview_questions(topic: str, interview_type: str, difficulty: int, language: str) -> list:
    """Generate interview questions based on parameters"""
    
    # Predefined questions based on topic and type
    question_bank = {
        'en': {
            'Personal Background': [
                "Tell me about yourself and your background.",
                "What motivates you to join government service?",
                "Describe your strengths and weaknesses.",
                "How do you handle pressure and stressful situations?",
                "What are your long-term career goals?"
            ],
            'Career Goals': [
                "Why do you want to work in the government sector?",
                "How do you see yourself contributing to public service?",
                "What changes would you like to bring in your department?",
                "How do you balance personal ambitions with public service?",
                "Describe your ideal work environment."
            ],
            'Current Affairs': [
                "What is your opinion on the latest government policies?",
                "How do current economic trends affect governance?",
                "Discuss a recent international event and its impact on India.",
                "What are the major challenges facing India today?",
                "How should the government address unemployment?"
            ],
            'Leadership': [
                "Describe a situation where you demonstrated leadership.",
                "How do you motivate a team during challenging times?",
                "What is the difference between a manager and a leader?",
                "How do you handle conflicts within your team?",
                "Give an example of a difficult decision you had to make."
            ],
            'Ethics': [
                "How do you handle ethical dilemmas in the workplace?",
                "What would you do if asked to compromise your values?",
                "Describe a situation where you stood up for what's right.",
                "How important is transparency in government work?",
                "What does integrity mean to you?"
            ]
        },
        'hi': {
            'Personal Background': [
                "अपने बारे में और अपनी पृष्ठभूमि के बारे में बताएं।",
                "आपको सरकारी सेवा में शामिल होने की प्रेरणा क्या देती है?",
                "अपनी शक्तियों और कमजोरियों का वर्णन करें।",
                "आप दबाव और तनावपूर्ण परिस्थितियों को कैसे संभालते हैं?",
                "आपके दीर्घकालिक करियर लक्ष्य क्या हैं?"
            ],
            'Career Goals': [
                "आप सरकारी क्षेत्र में क्यों काम करना चाहते हैं?",
                "आप लोक सेवा में अपना योगदान कैसे देखते हैं?",
                "आप अपने विभाग में क्या बदलाव लाना चाहेंगे?",
                "आप व्यक्तिगत महत्वाकांक्षाओं और लोक सेवा के बीच संतुलन कैसे बनाते हैं?",
                "अपने आदर्श कार्य वातावरण का वर्णन करें।"
            ],
            'Current Affairs': [
                "नवीनतम सरकारी नीतियों पर आपकी क्या राय है?",
                "वर्तमान आर्थिक रुझान शासन को कैसे प्रभावित करते हैं?",
                "हाल की किसी अंतर्राष्ट्रीय घटना और भारत पर इसके प्रभाव पर चर्चा करें।",
                "आज भारत के सामने मुख्य चुनौतियां क्या हैं?",
                "सरकार को बेरोजगारी की समस्या कैसे हल करनी चाहिए?"
            ],
            'Leadership': [
                "एक ऐसी स्थिति का वर्णन करें जहां आपने नेतृत्व का प्रदर्शन किया।",
                "चुनौतीपूर्ण समय में आप टीम को कैसे प्रेरित करते हैं?",
                "एक प्रबंधक और एक नेता के बीच क्या अंतर है?",
                "आप अपनी टीम के भीतर संघर्षों को कैसे संभालते हैं?",
                "किसी कठिन निर्णय का उदाहरण दें जो आपको लेना पड़ा।"
            ],
            'Ethics': [
                "आप कार्यस्थल में नैतिक दुविधाओं को कैसे संभालते हैं?",
                "यदि आपसे अपने मूल्यों से समझौता करने को कहा जाए तो आप क्या करेंगे?",
                "एक ऐसी स्थिति का वर्णन करें जहां आपने सही के लिए खड़े होकर समर्थन किया।",
                "सरकारी काम में पारदर्शिता कितनी महत्वपूर्ण है?",
                "आपके लिए ईमानदारी का क्या मतलब है?"
            ]
        }
    }
    
    # Get questions for the topic
    lang_key = 'hi' if language == 'hi' else 'en'
    topic_questions = question_bank.get(lang_key, {}).get(topic, question_bank[lang_key]['Personal Background'])
    
    # Select questions based on difficulty (more questions for higher difficulty)
    num_questions = min(3 + difficulty, len(topic_questions))
    return topic_questions[:num_questions]

def display_interview_question(session: dict, ai_services: AIServices, lang_manager: LanguageManager):
    """Display current interview question and handle response"""
    
    current_q_idx = session['current_question']
    question = session['questions'][current_q_idx]
    language = session['language']
    
    # Progress indicator
    progress = (current_q_idx + 1) / len(session['questions'])
    st.progress(progress)
    st.markdown(f"**Question {current_q_idx + 1}/{len(session['questions'])}**")
    
    # Question display
    st.markdown(f"### 🎤 {question}")
    
    # Response input
    st.markdown(f"#### {lang_manager.get_text('record_answer', language)}")
    
    # Text response (primary method)
    user_response = st.text_area(
        "Your Response" if language == 'en' else "आपका उत्तर",
        height=150,
        key=f"response_{current_q_idx}",
        placeholder="Type your detailed response here..." if language == 'en' 
                   else "यहां अपना विस्तृत उत्तर टाइप करें..."
    )
    
    # Optional: Voice recording simulation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button(f"🎯 {lang_manager.get_text('submit_response', language)}", 
                    disabled=not user_response.strip(), use_container_width=True):
            # Evaluate response
            with st.spinner("Evaluating your response..." if language == 'en' else "आपके उत्तर का मूल्यांकन कर रहे हैं..."):
                feedback = ai_services.conduct_mock_interview(question, user_response, language)
            
            # Store response and feedback
            session['responses'].append({
                'question': question,
                'response': user_response,
                'feedback': feedback,
                'timestamp': datetime.now().isoformat()
            })
            
            # Show feedback
            display_question_feedback(feedback, language, lang_manager)
            
            # Move to next question
            session['current_question'] += 1
            
            # Brief pause before next question
            time.sleep(2)
            st.rerun()
    
    with col2:
        if st.button("⏭️ Skip", help="Skip this question"):
            session['responses'].append({
                'question': question,
                'response': "Skipped",
                'feedback': None,
                'timestamp': datetime.now().isoformat()
            })
            session['current_question'] += 1
            st.rerun()
    
    # Interview guidelines
    with st.expander("💡 Interview Guidelines" if language == 'en' else "💡 साक्षात्कार दिशानिर्देश"):
        guidelines = get_interview_guidelines(language)
        for guideline in guidelines:
            st.markdown(f"• {guideline}")

def display_question_feedback(feedback: dict, language: str, lang_manager: LanguageManager):
    """Display AI feedback for the current response"""
    
    if not feedback:
        return
    
    st.markdown("---")
    st.markdown(f"### 📝 {lang_manager.get_text('interview_feedback', language)}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Score
        score = feedback.get('score', 75)
        st.metric(lang_manager.get_text('score', language), f"{score}/100")
        
        # Score interpretation
        if score >= 90:
            st.success("Excellent response! 🌟")
        elif score >= 80:
            st.success("Very good response! 👏")
        elif score >= 70:
            st.info("Good response! 👍")
        elif score >= 60:
            st.warning("Average response. Room for improvement.")
        else:
            st.error("Needs significant improvement.")
    
    with col2:
        # Strengths
        if feedback.get('strengths'):
            st.markdown(f"**{lang_manager.get_text('strengths', language)}:**")
            for strength in feedback['strengths']:
                st.markdown(f"✅ {strength}")
    
    # Areas for improvement
    if feedback.get('improvements'):
        st.markdown(f"**{lang_manager.get_text('improvements', language)}:**")
        for improvement in feedback['improvements']:
            st.markdown(f"🔄 {improvement}")
    
    # Model answer
    if feedback.get('model_answer'):
        with st.expander(f"📖 {lang_manager.get_text('model_answer', language)}"):
            st.markdown(feedback['model_answer'])
    
    # Overall feedback
    if feedback.get('overall_feedback'):
        st.info(f"**{lang_manager.get_text('overall_feedback', language)}:** {feedback['overall_feedback']}")

def display_interview_results(session: dict, lang_manager: LanguageManager):
    """Display final interview results and comprehensive feedback"""
    
    language = session['language']
    
    st.markdown(f"## 🎉 Interview Completed!" if language == 'en' else "## 🎉 साक्षात्कार पूर्ण!")
    
    # Calculate overall performance
    scores = [resp['feedback']['score'] for resp in session['responses'] if resp['feedback']]
    overall_score = sum(scores) / len(scores) if scores else 0
    
    # Performance summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Score" if language == 'en' else "समग्र स्कोर", f"{overall_score:.1f}/100")
    
    with col2:
        interview_time = (time.time() - session['start_time']) / 60
        st.metric("Time Taken" if language == 'en' else "समय लिया", f"{interview_time:.1f} min")
    
    with col3:
        st.metric("Questions Answered" if language == 'en' else "उत्तर दिए गए प्रश्न", 
                 len([r for r in session['responses'] if r['response'] != 'Skipped']))
    
    # Performance evaluation
    st.markdown("---")
    st.markdown("### 📊 Performance Evaluation" if language == 'en' else "### 📊 प्रदर्शन मूल्यांकन")
    
    if overall_score >= 85:
        st.success("🏆 Outstanding performance! You're well-prepared for interviews." if language == 'en'
                  else "🏆 उत्कृष्ट प्रदर्शन! आप साक्षात्कार के लिए अच्छी तरह तैयार हैं।")
    elif overall_score >= 75:
        st.success("🌟 Very good performance! Minor improvements needed." if language == 'en'
                  else "🌟 बहुत अच्छा प्रदर्शन! मामूली सुधार की जरूरत है।")
    elif overall_score >= 65:
        st.info("👍 Good performance! Some areas need attention." if language == 'en'
               else "👍 अच्छा प्रदर्शन! कुछ क्षेत्रों पर ध्यान देने की जरूरत है।")
    else:
        st.warning("💪 Needs improvement. Keep practicing!" if language == 'en'
                  else "💪 सुधार की जरूरत है। अभ्यास जारी रखें!")
    
    # Detailed question-wise feedback
    with st.expander("📋 Detailed Question-wise Feedback" if language == 'en' else "📋 विस्तृत प्रश्न-वार फीडबैक"):
        for i, response in enumerate(session['responses']):
            st.markdown(f"#### Question {i+1}: {response['question']}")
            
            if response['response'] == 'Skipped':
                st.warning("This question was skipped." if language == 'en' else "यह प्रश्न छोड़ दिया गया था।")
            else:
                st.markdown(f"**Your Response:** {response['response']}")
                
                if response['feedback']:
                    feedback = response['feedback']
                    st.markdown(f"**Score:** {feedback.get('score', 'N/A')}/100")
                    
                    if feedback.get('overall_feedback'):
                        st.info(feedback['overall_feedback'])
            
            st.divider()
    
    # Save interview results
    data_manager = DataManager()
    data_manager.save_interview_result(overall_score, session['topic'], language)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Another Interview" if language == 'en' else "🔄 दूसरा साक्षात्कार", use_container_width=True):
            if 'interview_session' in st.session_state:
                del st.session_state.interview_session
            st.rerun()
    
    with col2:
        if st.button("📊 View Analytics" if language == 'en' else "📊 विश्लेषण देखें", use_container_width=True):
            st.session_state.page = 'Analytics'
            st.rerun()
    
    with col3:
        if st.button("🏠 Home" if language == 'en' else "🏠 होम", use_container_width=True):
            if 'interview_session' in st.session_state:
                del st.session_state.interview_session
            st.session_state.page = 'Home'
            st.rerun()

def get_interview_tips(language: str) -> list:
    """Get interview tips based on language"""
    
    if language == 'hi':
        return [
            "आत्मविश्वास से बोलें और आंखों में आंखें डालकर बात करें",
            "प्रश्न को ध्यान से सुनें और समझकर उत्तर दें",
            "अपने उत्तर में व्यावहारिक उदाहरण शामिल करें",
            "सकारात्मक भाषा का प्रयोग करें और नकारात्मकता से बचें",
            "समसामयिक घटनाओं की जानकारी रखें",
            "शांत रहें और तनाव न लें",
            "ईमानदारी से उत्तर दें, कुछ भी गलत न बोलें",
            "समय का ध्यान रखें और संक्षिप्त उत्तर दें"
        ]
    else:
        return [
            "Speak confidently and maintain eye contact",
            "Listen carefully to questions and think before answering",
            "Include practical examples in your responses",
            "Use positive language and avoid negativity",
            "Stay updated with current affairs",
            "Remain calm and composed under pressure",
            "Be honest and authentic in your answers",
            "Manage time well and give concise responses"
        ]

def get_interview_guidelines(language: str) -> list:
    """Get interview guidelines based on language"""
    
    if language == 'hi':
        return [
            "स्पष्ट और धीमी गति से बोलें",
            "प्रश्न को पूरी तरह समझने के बाद उत्तर दें",
            "अपने व्यक्तिगत अनुभव साझा करें",
            "सरकारी नीतियों और योजनाओं की जानकारी दिखाएं",
            "नेतृत्व और टीम वर्क के उदाहरण दें",
            "समस्या समाधान की क्षमता प्रदर्शित करें"
        ]
    else:
        return [
            "Speak clearly and at a moderate pace",
            "Fully understand the question before responding",
            "Share your personal experiences and examples",
            "Demonstrate knowledge of government policies",
            "Provide examples of leadership and teamwork",
            "Show problem-solving abilities and analytical thinking"
        ]
