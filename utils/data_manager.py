import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

class DataManager:
    """Manages user data and application state using Streamlit session state"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables if they don't exist"""
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {
                'name': '',
                'exam_type': '',
                'target_date': None,
                'study_hours_per_day': 2,
                'quiz_scores': [],
                'study_streaks': 0,
                'badges': [],
                'total_points': 0,
                'last_activity': None,
                'topics_studied': {},
                'interview_scores': [],
                'current_affairs_score': 0
            }
        
        if 'quiz_history' not in st.session_state:
            st.session_state.quiz_history = []
        
        if 'study_plan' not in st.session_state:
            st.session_state.study_plan = {}
        
        if 'achievements' not in st.session_state:
            st.session_state.achievements = []
    
    def save_quiz_result(self, topic: str, score: int, total_questions: int, difficulty: int, language: str):
        """Save quiz result to user data"""
        quiz_result = {
            'topic': topic,
            'score': score,
            'total_questions': total_questions,
            'percentage': (score / total_questions) * 100,
            'difficulty': difficulty,
            'language': language,
            'date': datetime.now().isoformat(),
            'points_earned': self._calculate_points(score, total_questions, difficulty)
        }
        
        st.session_state.quiz_history.append(quiz_result)
        st.session_state.user_data['quiz_scores'].append(quiz_result['percentage'])
        st.session_state.user_data['total_points'] += quiz_result['points_earned']
        
        # Update topics studied
        if topic not in st.session_state.user_data['topics_studied']:
            st.session_state.user_data['topics_studied'][topic] = []
        st.session_state.user_data['topics_studied'][topic].append(quiz_result['percentage'])
        
        # Check for achievements
        self._check_achievements()
        
        # Update study streak
        self._update_study_streak()
    
    def save_interview_result(self, score: int, topic: str, language: str):
        """Save mock interview result"""
        interview_result = {
            'score': score,
            'topic': topic,
            'language': language,
            'date': datetime.now().isoformat(),
            'points_earned': score // 10  # 1 point per 10 score points
        }
        
        st.session_state.user_data['interview_scores'].append(interview_result)
        st.session_state.user_data['total_points'] += interview_result['points_earned']
        
        self._check_achievements()
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        quiz_scores = st.session_state.user_data['quiz_scores']
        
        stats = {
            'total_quizzes': len(quiz_scores),
            'average_score': sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0,
            'best_score': max(quiz_scores) if quiz_scores else 0,
            'total_points': st.session_state.user_data['total_points'],
            'study_streak': st.session_state.user_data['study_streaks'],
            'badges_count': len(st.session_state.user_data['badges']),
            'topics_mastered': len([topic for topic, scores in st.session_state.user_data['topics_studied'].items() 
                                  if sum(scores) / len(scores) >= 80]),
            'recent_activity': self._get_recent_activity(),
            'performance_trend': self._get_performance_trend(),
            'weak_topics': self._get_weak_topics(),
            'strong_topics': self._get_strong_topics()
        }
        
        return stats
    
    def get_quiz_history(self, limit: int = None) -> List[Dict]:
        """Get quiz history with optional limit"""
        history = st.session_state.quiz_history
        if limit:
            return history[-limit:]
        return history
    
    def get_topic_performance(self, topic: str) -> Dict[str, Any]:
        """Get performance data for a specific topic"""
        if topic not in st.session_state.user_data['topics_studied']:
            return {'attempts': 0, 'average_score': 0, 'best_score': 0, 'improvement': 0}
        
        scores = st.session_state.user_data['topics_studied'][topic]
        
        return {
            'attempts': len(scores),
            'average_score': sum(scores) / len(scores),
            'best_score': max(scores),
            'latest_score': scores[-1],
            'improvement': scores[-1] - scores[0] if len(scores) > 1 else 0
        }
    
    def _calculate_points(self, score: int, total: int, difficulty: int) -> int:
        """Calculate points earned based on performance and difficulty"""
        base_points = (score / total) * 100
        difficulty_multiplier = 1 + (difficulty - 1) * 0.2  # 1.0 to 1.8 multiplier
        return int(base_points * difficulty_multiplier)
    
    def _check_achievements(self):
        """Check and award achievements based on performance"""
        badges = st.session_state.user_data['badges']
        total_points = st.session_state.user_data['total_points']
        quiz_count = len(st.session_state.user_data['quiz_scores'])
        
        # Points-based badges
        if total_points >= 1000 and "🏆 Point Master" not in badges:
            badges.append("🏆 Point Master")
            st.success("Achievement Unlocked: 🏆 Point Master (1000+ points)")
        
        if total_points >= 500 and "⭐ Rising Star" not in badges:
            badges.append("⭐ Rising Star")
            st.success("Achievement Unlocked: ⭐ Rising Star (500+ points)")
        
        # Quiz-based badges
        if quiz_count >= 50 and "📚 Quiz Master" not in badges:
            badges.append("📚 Quiz Master")
            st.success("Achievement Unlocked: 📚 Quiz Master (50+ quizzes)")
        
        if quiz_count >= 10 and "🎯 Dedicated Learner" not in badges:
            badges.append("🎯 Dedicated Learner")
            st.success("Achievement Unlocked: 🎯 Dedicated Learner (10+ quizzes)")
        
        # Perfect score badges
        perfect_scores = [score for score in st.session_state.user_data['quiz_scores'] if score == 100]
        if len(perfect_scores) >= 5 and "💯 Perfectionist" not in badges:
            badges.append("💯 Perfectionist")
            st.success("Achievement Unlocked: 💯 Perfectionist (5 perfect scores)")
        
        # Streak badges
        if st.session_state.user_data['study_streaks'] >= 7 and "🔥 Week Warrior" not in badges:
            badges.append("🔥 Week Warrior")
            st.success("Achievement Unlocked: 🔥 Week Warrior (7-day streak)")
    
    def _update_study_streak(self):
        """Update study streak based on activity"""
        today = datetime.now().date()
        last_activity = st.session_state.user_data.get('last_activity')
        
        if last_activity:
            last_date = datetime.fromisoformat(last_activity).date()
            days_diff = (today - last_date).days
            
            if days_diff == 1:
                # Consecutive day
                st.session_state.user_data['study_streaks'] += 1
            elif days_diff > 1:
                # Streak broken
                st.session_state.user_data['study_streaks'] = 1
        else:
            # First activity
            st.session_state.user_data['study_streaks'] = 1
        
        st.session_state.user_data['last_activity'] = today.isoformat()
    
    def _get_recent_activity(self) -> List[Dict]:
        """Get recent user activity"""
        recent_quizzes = st.session_state.quiz_history[-5:] if st.session_state.quiz_history else []
        return [
            {
                'type': 'Quiz',
                'topic': quiz['topic'],
                'score': f"{quiz['score']}/{quiz['total_questions']}",
                'date': datetime.fromisoformat(quiz['date']).strftime('%Y-%m-%d %H:%M')
            }
            for quiz in recent_quizzes
        ]
    
    def _get_performance_trend(self) -> List[float]:
        """Get performance trend for the last 10 quizzes"""
        scores = st.session_state.user_data['quiz_scores']
        return scores[-10:] if len(scores) >= 10 else scores
    
    def _get_weak_topics(self) -> List[str]:
        """Identify topics where user performance is below average"""
        topics_studied = st.session_state.user_data['topics_studied']
        weak_topics = []
        
        for topic, scores in topics_studied.items():
            if scores and sum(scores) / len(scores) < 60:  # Below 60% average
                weak_topics.append(topic)
        
        return weak_topics
    
    def _get_strong_topics(self) -> List[str]:
        """Identify topics where user performance is above average"""
        topics_studied = st.session_state.user_data['topics_studied']
        strong_topics = []
        
        for topic, scores in topics_studied.items():
            if scores and sum(scores) / len(scores) >= 80:  # Above 80% average
                strong_topics.append(topic)
        
        return strong_topics
    
    def export_user_data(self) -> str:
        """Export user data as JSON string"""
        export_data = {
            'user_data': st.session_state.user_data,
            'quiz_history': st.session_state.quiz_history,
            'study_plan': st.session_state.study_plan,
            'export_date': datetime.now().isoformat()
        }
        return json.dumps(export_data, indent=2)
    
    def import_user_data(self, data_json: str) -> bool:
        """Import user data from JSON string"""
        try:
            data = json.loads(data_json)
            st.session_state.user_data = data.get('user_data', {})
            st.session_state.quiz_history = data.get('quiz_history', [])
            st.session_state.study_plan = data.get('study_plan', {})
            return True
        except Exception as e:
            st.error(f"Error importing data: {str(e)}")
            return False
