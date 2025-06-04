import streamlit as st
from utils.ai_services import AIServices
from utils.data_manager import DataManager
from utils.language_manager import LanguageManager
from datetime import datetime, timedelta
import pandas as pd

def show_study_plan_page(language: str, lang_manager: LanguageManager):
    """Display the personalized study plan page"""
    
    ai_services = AIServices()
    data_manager = DataManager()
    
    st.markdown(f"## 🎯 {lang_manager.get_text('personalized_study_plan', language)}")
    
    # Check if user has profile data
    user_data = st.session_state.user_data
    if not user_data.get('name') or not user_data.get('exam_type'):
        st.warning("Please complete your profile setup in the Home page to generate a personalized study plan." if language == 'en' 
                  else "व्यक्तिगत अध्ययन योजना बनाने के लिए कृपया होम पेज में अपना प्रोफाइल सेटअप पूरा करें।")
        return
    
    # Display user info
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### 👤 {user_data['name']}")
        st.markdown(f"**{lang_manager.get_text('target_exam', language)}:** {user_data['exam_type']}")
        st.markdown(f"**{lang_manager.get_text('daily_study_hours', language)}:** {user_data['study_hours_per_day']} hours")
        if user_data.get('target_date'):
            days_left = (user_data['target_date'] - datetime.now().date()).days
            st.markdown(f"**Days until exam:** {days_left} days" if language == 'en' 
                       else f"**परीक्षा तक दिन:** {days_left} दिन")
    
    with col2:
        # Generate study plan button
        if st.button(f"🚀 {lang_manager.get_text('generate_study_plan', language)}", use_container_width=True):
            generate_study_plan(user_data, language, ai_services, lang_manager)
    
    # Display existing study plan if available
    if st.session_state.get('study_plan'):
        display_study_plan(st.session_state.study_plan, language, lang_manager)
    
    # Study statistics
    display_study_statistics(data_manager, language, lang_manager)

def generate_study_plan(user_data: dict, language: str, ai_services: AIServices, lang_manager: LanguageManager):
    """Generate AI-powered study plan"""
    
    with st.spinner(lang_manager.get_text('loading', language)):
        study_plan = ai_services.generate_study_plan(user_data, language)
    
    if study_plan:
        st.session_state.study_plan = study_plan
        st.success("Study plan generated successfully!" if language == 'en' 
                  else "अध्ययन योजना सफलतापूर्वक तैयार की गई!")
        st.rerun()
    else:
        st.error("Failed to generate study plan. Please try again." if language == 'en'
                else "अध्ययन योजना बनाने में असफल। कृपया पुनः प्रयास करें।")

def display_study_plan(study_plan: dict, language: str, lang_manager: LanguageManager):
    """Display the generated study plan"""
    
    st.markdown("---")
    
    # Daily Schedule
    if study_plan.get('daily_schedule'):
        st.markdown(f"### 📅 {lang_manager.get_text('daily_schedule', language)}")
        
        # Create dataframe for better display
        schedule_data = []
        for item in study_plan['daily_schedule']:
            schedule_data.append({
                lang_manager.get_text('time_slot', language): item.get('time_slot', ''),
                lang_manager.get_text('subject', language): item.get('subject', ''),
                lang_manager.get_text('duration', language): item.get('duration', ''),
                lang_manager.get_text('activity', language): item.get('activity', ''),
                lang_manager.get_text('priority', language): item.get('priority', '')
            })
        
        if schedule_data:
            df = pd.DataFrame(schedule_data)
            st.dataframe(df, use_container_width=True)
        
        # Visual timeline
        st.markdown("#### 📊 Study Timeline")
        col1, col2, col3 = st.columns(3)
        
        morning_tasks = [item for item in study_plan['daily_schedule'] if 'morning' in item.get('time_slot', '').lower()]
        afternoon_tasks = [item for item in study_plan['daily_schedule'] if 'afternoon' in item.get('time_slot', '').lower()]
        evening_tasks = [item for item in study_plan['daily_schedule'] if 'evening' in item.get('time_slot', '').lower()]
        
        with col1:
            st.markdown("**🌅 Morning**" if language == 'en' else "**🌅 सुबह**")
            for task in morning_tasks:
                st.markdown(f"• {task.get('subject', '')} ({task.get('duration', '')})")
        
        with col2:
            st.markdown("**🌞 Afternoon**" if language == 'en' else "**🌞 दोपहर**")
            for task in afternoon_tasks:
                st.markdown(f"• {task.get('subject', '')} ({task.get('duration', '')})")
        
        with col3:
            st.markdown("**🌙 Evening**" if language == 'en' else "**🌙 शाम**")
            for task in evening_tasks:
                st.markdown(f"• {task.get('subject', '')} ({task.get('duration', '')})")
    
    # Weekly Goals
    if study_plan.get('weekly_goals'):
        st.markdown(f"### 🎯 {lang_manager.get_text('weekly_goals', language)}")
        for i, goal in enumerate(study_plan['weekly_goals'], 1):
            st.markdown(f"{i}. {goal}")
    
    # Recommended Topics
    if study_plan.get('recommended_topics'):
        st.markdown(f"### 📚 {lang_manager.get_text('recommended_topics', language)}")
        
        # Display as cards
        cols = st.columns(3)
        for i, topic in enumerate(study_plan['recommended_topics']):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(45deg, #FF9933, #138808);
                    color: white;
                    padding: 1rem;
                    border-radius: 10px;
                    text-align: center;
                    margin: 0.5rem 0;
                    font-weight: bold;
                ">
                    {topic}
                </div>
                """, unsafe_allow_html=True)
    
    # Study Tips
    if study_plan.get('study_tips'):
        st.markdown(f"### 💡 {lang_manager.get_text('study_tips', language)}")
        for tip in study_plan['study_tips']:
            st.markdown(f"💡 {tip}")

def display_study_statistics(data_manager: DataManager, language: str, lang_manager: LanguageManager):
    """Display study statistics and progress tracking"""
    
    st.markdown("---")
    st.markdown(f"### 📈 Study Progress" if language == 'en' else "### 📈 अध्ययन प्रगति")
    
    stats = data_manager.get_user_stats()
    
    # Progress metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            lang_manager.get_text('total_attempts', language),
            stats['total_quizzes']
        )
    
    with col2:
        st.metric(
            lang_manager.get_text('average_score', language),
            f"{stats['average_score']:.1f}%"
        )
    
    with col3:
        st.metric(
            "Topics Mastered" if language == 'en' else "महारत के विषय",
            stats['topics_mastered']
        )
    
    with col4:
        st.metric(
            lang_manager.get_text('study_streak', language),
            f"{stats['study_streak']} {lang_manager.get_text('days', language)}"
        )
    
    # Performance trend chart
    if stats['performance_trend']:
        st.markdown("#### 📊 Performance Trend" if language == 'en' else "#### 📊 प्रदर्शन रुझान")
        
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, len(stats['performance_trend']) + 1)),
            y=stats['performance_trend'],
            mode='lines+markers',
            name='Score %',
            line=dict(color='#FF9933'),
            marker=dict(color='#138808')
        ))
        
        fig.update_layout(
            title="Recent Quiz Scores" if language == 'en' else "हाल के क्विज़ स्कोर",
            xaxis_title="Quiz Number" if language == 'en' else "क्विज़ संख्या",
            yaxis_title="Score %" if language == 'en' else "स्कोर %",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Topic analysis
    col1, col2 = st.columns(2)
    
    with col1:
        if stats['strong_topics']:
            st.markdown(f"#### 💪 {lang_manager.get_text('strong_topics', language)}")
            for topic in stats['strong_topics']:
                st.success(f"✅ {topic}")
    
    with col2:
        if stats['weak_topics']:
            st.markdown(f"#### 🎯 {lang_manager.get_text('weak_topics', language)}")
            for topic in stats['weak_topics']:
                st.warning(f"⚠️ {topic}")
    
    # Study recommendations
    st.markdown("#### 📋 Personalized Recommendations" if language == 'en' else "#### 📋 व्यक्तिगत सिफारिशें")
    
    recommendations = generate_recommendations(stats, language)
    for rec in recommendations:
        st.info(f"💡 {rec}")

def generate_recommendations(stats: dict, language: str) -> list:
    """Generate personalized study recommendations based on performance"""
    
    recommendations = []
    
    if language == 'hi':
        if stats['average_score'] < 60:
            recommendations.append("मूलभूत अवधारणाओं पर अधिक ध्यान दें और दैनिक अभ्यास बढ़ाएं")
        elif stats['average_score'] < 80:
            recommendations.append("अच्छी प्रगति! अब कठिन प्रश्नों का अभ्यास करें")
        else:
            recommendations.append("उत्कृष्ट! उच्च कठिनाई स्तर के प्रश्नों का प्रयास करें")
        
        if stats['study_streak'] < 3:
            recommendations.append("नियमित अध्ययन की आदत बनाने के लिए दैनिक छोटे सत्र रखें")
        
        if stats['total_quizzes'] < 10:
            recommendations.append("अधिक क्विज़ लेकर अपने ज्ञान का परीक्षण करें")
        
        if stats['weak_topics']:
            recommendations.append(f"कमजोर विषयों पर विशेष ध्यान दें: {', '.join(stats['weak_topics'][:3])}")
    else:
        if stats['average_score'] < 60:
            recommendations.append("Focus on fundamental concepts and increase daily practice time")
        elif stats['average_score'] < 80:
            recommendations.append("Good progress! Now practice more challenging questions")
        else:
            recommendations.append("Excellent! Try higher difficulty levels and mentor others")
        
        if stats['study_streak'] < 3:
            recommendations.append("Build a consistent study habit with daily short sessions")
        
        if stats['total_quizzes'] < 10:
            recommendations.append("Take more quizzes to better assess your knowledge")
        
        if stats['weak_topics']:
            recommendations.append(f"Focus on improving weak topics: {', '.join(stats['weak_topics'][:3])}")
    
    return recommendations
