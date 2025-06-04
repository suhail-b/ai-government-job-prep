import streamlit as st
from utils.data_manager import DataManager
from utils.language_manager import LanguageManager
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

def show_analytics_page(language: str, lang_manager: LanguageManager):
    """Display comprehensive performance analytics"""
    
    data_manager = DataManager()
    
    st.markdown(f"## 📊 {lang_manager.get_text('performance_analytics', language)}")
    
    # Get user statistics
    stats = data_manager.get_user_stats()
    quiz_history = data_manager.get_quiz_history()
    
    if not quiz_history:
        st.info("No quiz data available. Take some quizzes to see your analytics!" if language == 'en'
               else "कोई क्विज़ डेटा उपलब्ध नहीं है। अपने विश्लेषण देखने के लिए कुछ क्विज़ लें!")
        return
    
    # Overview metrics
    display_overview_metrics(stats, language, lang_manager)
    
    # Performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        display_performance_trend(quiz_history, language, lang_manager)
    
    with col2:
        display_topic_performance(quiz_history, language, lang_manager)
    
    # Detailed analytics
    display_difficulty_analysis(quiz_history, language, lang_manager)
    display_time_based_analysis(quiz_history, language, lang_manager)
    display_achievement_progress(stats, language, lang_manager)

def display_overview_metrics(stats: dict, language: str, lang_manager: LanguageManager):
    """Display key performance metrics"""
    
    st.markdown(f"### 🎯 {lang_manager.get_text('overall_performance', language)}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_score = None
        if len(st.session_state.user_data['quiz_scores']) >= 2:
            recent_scores = st.session_state.user_data['quiz_scores'][-5:]
            prev_scores = st.session_state.user_data['quiz_scores'][-10:-5] if len(st.session_state.user_data['quiz_scores']) >= 10 else []
            if prev_scores:
                recent_avg = sum(recent_scores) / len(recent_scores)
                prev_avg = sum(prev_scores) / len(prev_scores)
                delta_score = recent_avg - prev_avg
        
        st.metric(
            lang_manager.get_text('average_score', language),
            f"{stats['average_score']:.1f}%",
            delta=f"{delta_score:+.1f}%" if delta_score else None
        )
    
    with col2:
        st.metric(
            lang_manager.get_text('best_score', language),
            f"{stats['best_score']:.1f}%"
        )
    
    with col3:
        st.metric(
            lang_manager.get_text('total_attempts', language),
            stats['total_quizzes']
        )
    
    with col4:
        st.metric(
            lang_manager.get_text('total_points', language),
            stats['total_points']
        )
    
    # Performance gauge
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = stats['average_score'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall Performance" if language == 'en' else "समग्र प्रदर्शन"},
        delta = {'reference': 60},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#FF9933"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "#138808"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

def display_performance_trend(quiz_history: list, language: str, lang_manager: LanguageManager):
    """Display performance trend over time"""
    
    st.markdown(f"#### 📈 {lang_manager.get_text('performance_trend', language)}")
    
    if len(quiz_history) < 2:
        st.info("Take more quizzes to see performance trends!" if language == 'en'
               else "प्रदर्शन रुझान देखने के लिए अधिक क्विज़ लें!")
        return
    
    # Prepare data
    dates = [datetime.fromisoformat(quiz['date']).date() for quiz in quiz_history]
    scores = [quiz['percentage'] for quiz in quiz_history]
    
    # Create trend line
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        name='Quiz Scores',
        line=dict(color='#FF9933', width=3),
        marker=dict(color='#138808', size=8)
    ))
    
    # Add trend line
    if len(scores) > 3:
        z = np.polyfit(range(len(scores)), scores, 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=dates,
            y=p(range(len(scores))),
            mode='lines',
            name='Trend',
            line=dict(color='red', width=2, dash='dash')
        ))
    
    fig.update_layout(
        title="Score Progression" if language == 'en' else "स्कोर प्रगति",
        xaxis_title="Date" if language == 'en' else "दिनांक",
        yaxis_title="Score %" if language == 'en' else "स्कोर %",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_topic_performance(quiz_history: list, language: str, lang_manager: LanguageManager):
    """Display performance by topic"""
    
    st.markdown(f"#### 📚 {lang_manager.get_text('topic_wise_performance', language)}")
    
    # Calculate topic averages
    topic_scores = {}
    topic_counts = {}
    
    for quiz in quiz_history:
        topic = quiz['topic']
        score = quiz['percentage']
        
        if topic not in topic_scores:
            topic_scores[topic] = []
            topic_counts[topic] = 0
        
        topic_scores[topic].append(score)
        topic_counts[topic] += 1
    
    # Calculate averages
    topic_averages = {topic: sum(scores)/len(scores) for topic, scores in topic_scores.items()}
    
    # Create bar chart
    topics = list(topic_averages.keys())
    averages = list(topic_averages.values())
    counts = [topic_counts[topic] for topic in topics]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=topics,
        y=averages,
        text=[f"{avg:.1f}% ({cnt} attempts)" for avg, cnt in zip(averages, counts)],
        textposition='auto',
        marker_color=['#138808' if avg >= 80 else '#FF9933' if avg >= 60 else '#FF6B6B' for avg in averages]
    ))
    
    fig.update_layout(
        title="Average Score by Topic" if language == 'en' else "विषयवार औसत स्कोर",
        xaxis_title="Topics" if language == 'en' else "विषय",
        yaxis_title="Average Score %" if language == 'en' else "औसत स्कोर %",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_difficulty_analysis(quiz_history: list, language: str, lang_manager: LanguageManager):
    """Analyze performance by difficulty level"""
    
    st.markdown("---")
    st.markdown("### 🎚️ Difficulty Level Analysis" if language == 'en' else "### 🎚️ कठिनाई स्तर विश्लेषण")
    
    # Group by difficulty
    difficulty_data = {}
    for quiz in quiz_history:
        diff = quiz.get('difficulty', 3)
        if diff not in difficulty_data:
            difficulty_data[diff] = []
        difficulty_data[diff].append(quiz['percentage'])
    
    if difficulty_data:
        col1, col2 = st.columns(2)
        
        with col1:
            # Box plot for difficulty distribution
            fig = go.Figure()
            
            for diff in sorted(difficulty_data.keys()):
                fig.add_trace(go.Box(
                    y=difficulty_data[diff],
                    name=f"Level {diff}",
                    boxpoints='all',
                    jitter=0.3,
                    pointpos=-1.8
                ))
            
            fig.update_layout(
                title="Score Distribution by Difficulty" if language == 'en' else "कठिनाई के अनुसार स्कोर वितरण",
                yaxis_title="Score %" if language == 'en' else "स्कोर %",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Average by difficulty
            diff_avg = {diff: sum(scores)/len(scores) for diff, scores in difficulty_data.items()}
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=[f"Level {d}" for d in sorted(diff_avg.keys())],
                y=[diff_avg[d] for d in sorted(diff_avg.keys())],
                text=[f"{diff_avg[d]:.1f}%" for d in sorted(diff_avg.keys())],
                textposition='auto',
                marker_color='#FF9933'
            ))
            
            fig.update_layout(
                title="Average Score by Difficulty" if language == 'en' else "कठिनाई के अनुसार औसत स्कोर",
                xaxis_title="Difficulty Level" if language == 'en' else "कठिनाई स्तर",
                yaxis_title="Average Score %" if language == 'en' else "औसत स्कोर %",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

def display_time_based_analysis(quiz_history: list, language: str, lang_manager: LanguageManager):
    """Analyze performance over time periods"""
    
    st.markdown("### 📅 Time-based Analysis" if language == 'en' else "### 📅 समय-आधारित विश्लेषण")
    
    # Group by week
    weekly_data = {}
    for quiz in quiz_history:
        date = datetime.fromisoformat(quiz['date']).date()
        # Get week start (Monday)
        week_start = date - timedelta(days=date.weekday())
        week_key = week_start.strftime("%Y-W%U")
        
        if week_key not in weekly_data:
            weekly_data[week_key] = []
        weekly_data[week_key].append(quiz['percentage'])
    
    if len(weekly_data) > 1:
        weeks = sorted(weekly_data.keys())
        weekly_avg = [sum(weekly_data[week])/len(weekly_data[week]) for week in weeks]
        weekly_count = [len(weekly_data[week]) for week in weeks]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Weekly average scores
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=weeks,
                y=weekly_avg,
                mode='lines+markers',
                name='Weekly Average',
                line=dict(color='#138808'),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                title="Weekly Performance" if language == 'en' else "साप्ताहिक प्रदर्शन",
                xaxis_title="Week" if language == 'en' else "सप्ताह",
                yaxis_title="Average Score %" if language == 'en' else "औसत स्कोर %",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Quiz frequency
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=weeks,
                y=weekly_count,
                text=weekly_count,
                textposition='auto',
                marker_color='#FF9933'
            ))
            
            fig.update_layout(
                title="Quiz Frequency by Week" if language == 'en' else "साप्ताहिक क्विज़ आवृत्ति",
                xaxis_title="Week" if language == 'en' else "सप्ताह",
                yaxis_title="Number of Quizzes" if language == 'en' else "क्विज़ की संख्या",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)

def display_achievement_progress(stats: dict, language: str, lang_manager: LanguageManager):
    """Display achievement progress and goals"""
    
    st.markdown("---")
    st.markdown(f"### 🏆 {lang_manager.get_text('achievements', language)} & Goals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Achievement Progress")
        
        # Points progress
        points_milestones = [100, 500, 1000, 2500, 5000]
        current_points = stats['total_points']
        
        for milestone in points_milestones:
            progress = min(current_points / milestone, 1.0)
            st.progress(progress)
            st.markdown(f"**{milestone} Points Goal:** {current_points}/{milestone} ({progress*100:.1f}%)")
        
        # Quiz milestones
        quiz_milestones = [10, 25, 50, 100, 200]
        current_quizzes = stats['total_quizzes']
        
        st.markdown("#### 📝 Quiz Milestones")
        for milestone in quiz_milestones:
            progress = min(current_quizzes / milestone, 1.0)
            if progress == 1.0:
                st.success(f"✅ {milestone} Quizzes Completed!")
            else:
                st.info(f"🎯 {milestone} Quizzes: {current_quizzes}/{milestone}")
    
    with col2:
        st.markdown("#### 📊 Performance Goals")
        
        current_avg = stats['average_score']
        performance_goals = [60, 70, 80, 90, 95]
        
        for goal in performance_goals:
            if current_avg >= goal:
                st.success(f"✅ Maintain {goal}%+ average")
            else:
                points_needed = goal - current_avg
                st.info(f"🎯 Reach {goal}% average (need +{points_needed:.1f}%)")
        
        # Streak goals
        st.markdown("#### 🔥 Study Streak Goals")
        streak_goals = [3, 7, 14, 30, 100]
        current_streak = stats['study_streak']
        
        for goal in streak_goals:
            if current_streak >= goal:
                st.success(f"✅ {goal}-day streak achieved!")
            else:
                st.info(f"🎯 {goal}-day streak goal")

# Import numpy for trend analysis
try:
    import numpy as np
except ImportError:
    st.error("NumPy is required for advanced analytics. Please install it.")
    np = None
