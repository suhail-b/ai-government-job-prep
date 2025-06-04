import streamlit as st
from utils.ai_services import AIServices
from utils.data_manager import DataManager
from utils.language_manager import LanguageManager
import time

def show_quiz_page(language: str, lang_manager: LanguageManager):
    """Display the AI Quiz page"""
    
    # Initialize services
    ai_services = AIServices()
    data_manager = DataManager()
    
    st.markdown(f"## 📝 {lang_manager.get_text('quiz_generator', language)}")
    
    # Quiz configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topics = lang_manager.get_quiz_topics(language)
        selected_topic = st.selectbox(
            lang_manager.get_text('select_topic', language),
            options=list(topics.keys()),
            key="quiz_topic"
        )
        
        difficulty = st.slider(
            lang_manager.get_text('select_difficulty', language),
            min_value=1,
            max_value=5,
            value=3,
            key="quiz_difficulty"
        )
        
        num_questions = st.selectbox(
            lang_manager.get_text('number_of_questions', language),
            options=[5, 10, 15, 20],
            index=0,
            key="num_questions"
        )
    
    with col2:
        # Display difficulty guide
        if language == 'hi':
            difficulty_guide = {
                1: "बहुत आसान - मूलभूत स्तर",
                2: "आसान - प्रारंभिक स्तर", 
                3: "मध्यम - मानक स्तर",
                4: "कठिन - उन्नत स्तर",
                5: "बहुत कठिन - विशेषज्ञ स्तर"
            }
        else:
            difficulty_guide = {
                1: "Very Easy - Basic Level",
                2: "Easy - Beginner Level",
                3: "Medium - Standard Level", 
                4: "Hard - Advanced Level",
                5: "Very Hard - Expert Level"
            }
        
        st.markdown("### 📊 Difficulty Guide")
        for level, desc in difficulty_guide.items():
            if level == difficulty:
                st.markdown(f"**{level}. {desc}** ⭐")
            else:
                st.markdown(f"{level}. {desc}")
    
    # Generate quiz button
    if st.button(f"🚀 {lang_manager.get_text('generate_quiz', language)}", use_container_width=True):
        generate_and_run_quiz(selected_topic, difficulty, num_questions, language, ai_services, data_manager, lang_manager)

def generate_and_run_quiz(topic: str, difficulty: int, num_questions: int, language: str, 
                         ai_services: AIServices, data_manager: DataManager, lang_manager: LanguageManager):
    """Generate and run a quiz session"""
    
    with st.spinner(lang_manager.get_text('loading', language)):
        questions = ai_services.generate_quiz_questions(topic, difficulty, language, num_questions)
    
    if not questions:
        st.error("Unable to generate quiz questions. Please check your OpenAI API key or try again later.")
        return
    
    # Initialize quiz session
    if 'quiz_session' not in st.session_state:
        st.session_state.quiz_session = {
            'questions': questions,
            'current_question': 0,
            'answers': [],
            'score': 0,
            'start_time': time.time(),
            'topic': topic,
            'difficulty': difficulty,
            'language': language
        }
    
    # Display current question
    session = st.session_state.quiz_session
    current_q_idx = session['current_question']
    
    if current_q_idx < len(session['questions']):
        display_question(session, current_q_idx, lang_manager, language)
    else:
        display_quiz_results(session, data_manager, lang_manager, language)

def display_question(session: dict, q_idx: int, lang_manager: LanguageManager, language: str):
    """Display current question and handle user interaction"""
    
    question = session['questions'][q_idx]
    
    # Progress bar
    progress = (q_idx + 1) / len(session['questions'])
    st.progress(progress)
    st.markdown(f"**{lang_manager.get_text('quiz', language)} {q_idx + 1}/{len(session['questions'])}**")
    
    # Question display
    st.markdown(f"### {question['question']}")
    
    # Answer options
    user_answer = st.radio(
        "Select your answer:",
        options=range(len(question['options'])),
        format_func=lambda x: f"{chr(65+x)}. {question['options'][x]}",
        key=f"question_{q_idx}"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(lang_manager.get_text('submit_answer', language), use_container_width=True):
            # Record answer
            is_correct = user_answer == question['correct_answer']
            session['answers'].append({
                'question_idx': q_idx,
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
            
            time.sleep(2)  # Brief pause to show result
            st.rerun()

def display_quiz_results(session: dict, data_manager: DataManager, lang_manager: LanguageManager, language: str):
    """Display quiz completion results and statistics"""
    
    score = session['score']
    total = len(session['questions'])
    percentage = (score / total) * 100
    time_taken = time.time() - session['start_time']
    
    # Celebration based on performance
    if percentage >= 90:
        st.balloons()
        performance_emoji = "🏆"
        performance_text = "Outstanding!" if language == 'en' else "उत्कृष्ट!"
    elif percentage >= 80:
        performance_emoji = "🌟"
        performance_text = "Excellent!" if language == 'en' else "बेहतरीन!"
    elif percentage >= 70:
        performance_emoji = "👏"
        performance_text = "Good Job!" if language == 'en' else "अच्छा काम!"
    elif percentage >= 60:
        performance_emoji = "👍"
        performance_text = "Not Bad!" if language == 'en' else "बुरा नहीं!"
    else:
        performance_emoji = "💪"
        performance_text = "Keep Practicing!" if language == 'en' else "अभ्यास जारी रखें!"
    
    st.markdown(f"# {performance_emoji} {lang_manager.get_text('quiz_completed', language)}")
    st.markdown(f"## {performance_text}")
    
    # Score display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(lang_manager.get_text('your_score', language), f"{score}/{total}")
    
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    
    with col3:
        st.metric("Time Taken" if language == 'en' else "समय लिया", f"{time_taken/60:.1f} min")
    
    with col4:
        points_earned = data_manager._calculate_points(score, total, session['difficulty'])
        st.metric(lang_manager.get_text('points_earned', language), points_earned)
    
    # Save results
    data_manager.save_quiz_result(
        topic=session['topic'],
        score=score,
        total_questions=total,
        difficulty=session['difficulty'],
        language=session['language']
    )
    
    # Detailed review
    with st.expander("📋 Detailed Review" if language == 'en' else "📋 विस्तृत समीक्षा", expanded=False):
        for i, answer in enumerate(session['answers']):
            question = session['questions'][answer['question_idx']]
            
            if answer['is_correct']:
                st.success(f"**Q{i+1}.** {answer['question_text']}")
                st.markdown(f"Your answer: ✅ {question['options'][answer['user_answer']]}")
            else:
                st.error(f"**Q{i+1}.** {answer['question_text']}")
                st.markdown(f"Your answer: ❌ {question['options'][answer['user_answer']]}")
                st.markdown(f"Correct answer: ✅ {question['options'][answer['correct_answer']]}")
            
            if answer['explanation']:
                st.info(f"💡 {answer['explanation']}")
            
            st.divider()
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Take Another Quiz" if language == 'en' else "🔄 दूसरी क्विज़ लें", use_container_width=True):
            # Clear quiz session
            if 'quiz_session' in st.session_state:
                del st.session_state.quiz_session
            st.rerun()
    
    with col2:
        if st.button("📊 View Analytics" if language == 'en' else "📊 विश्लेषण देखें", use_container_width=True):
            st.session_state.page = 'Analytics'
            st.rerun()
    
    with col3:
        if st.button("🏠 Go Home" if language == 'en' else "🏠 होम जाएं", use_container_width=True):
            if 'quiz_session' in st.session_state:
                del st.session_state.quiz_session
            st.session_state.page = 'Home'
            st.rerun()
    
    # Performance insights
    st.markdown("---")
    st.markdown(f"### 💡 {lang_manager.get_text('study_tips', language)}")
    
    if percentage < 60:
        tips = [
            "Focus on fundamentals and basic concepts" if language == 'en' else "मूलभूत और बुनियादी अवधारणाओं पर ध्यान दें",
            "Practice more questions on this topic" if language == 'en' else "इस विषय पर अधिक प्रश्नों का अभ्यास करें",
            "Review study materials thoroughly" if language == 'en' else "अध्ययन सामग्री की पूरी तरह समीक्षा करें"
        ]
    elif percentage < 80:
        tips = [
            "Good progress! Focus on weak areas" if language == 'en' else "अच्छी प्रगति! कमजोर क्षेत्रों पर ध्यान दें",
            "Practice advanced level questions" if language == 'en' else "उन्नत स्तर के प्रश्नों का अभ्यास करें",
            "Time management can be improved" if language == 'en' else "समय प्रबंधन में सुधार हो सकता है"
        ]
    else:
        tips = [
            "Excellent work! Maintain this level" if language == 'en' else "उत्कृष्ट कार्य! इस स्तर को बनाए रखें",
            "Try higher difficulty levels" if language == 'en' else "उच्च कठिनाई स्तर का प्रयास करें",
            "Help others and teach concepts" if language == 'en' else "दूसरों की मदद करें और अवधारणाएं सिखाएं"
        ]
    
    for tip in tips:
        st.markdown(f"• {tip}")
