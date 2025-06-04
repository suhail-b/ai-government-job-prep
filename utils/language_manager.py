from typing import Dict, Any

class LanguageManager:
    """Manages multilingual content for the application"""
    
    def __init__(self):
        self.translations = {
            'en': {
                # App main
                'app_title': 'AI Government Job Prep',
                'welcome_message': 'Welcome to AI-Powered Government Job Preparation',
                'app_description': '🎯 Prepare for Indian government exams with AI-powered quizzes, personalized study plans, and comprehensive analytics. Master UPSC, SSC, Banking, Railways, and other competitive exams with our intelligent learning platform.',
                
                # Navigation
                'home': 'Home',
                'quiz': 'AI Quiz',
                'study_plan': 'Study Plan',
                'analytics': 'Analytics',
                'mock_interview': 'Mock Interview',
                'current_affairs': 'Current Affairs',
                
                # Profile
                'profile_setup': 'Profile Setup',
                'your_name': 'Your Name',
                'target_exam': 'Target Exam',
                'target_date': 'Target Date',
                'daily_study_hours': 'Daily Study Hours',
                'save_profile': 'Save Profile',
                'profile_saved': 'Profile saved successfully!',
                
                # Quick stats
                'quick_stats': 'Quick Stats',
                'total_points': 'Total Points',
                'study_streak': 'Study Streak',
                'days': 'days',
                'quizzes_completed': 'Quizzes Completed',
                'achievements': 'Achievements',
                
                # Quick actions
                'quick_actions': 'Quick Actions',
                'take_quiz': 'Take Quiz',
                'view_progress': 'View Progress',
                'mock_interview': 'Mock Interview',
                
                # Quiz
                'quiz_generator': 'AI Quiz Generator',
                'select_topic': 'Select Topic',
                'select_difficulty': 'Select Difficulty (1-5)',
                'number_of_questions': 'Number of Questions',
                'generate_quiz': 'Generate Quiz',
                'submit_answer': 'Submit Answer',
                'next_question': 'Next Question',
                'quiz_completed': 'Quiz Completed!',
                'your_score': 'Your Score',
                'correct_answer': 'Correct Answer',
                'explanation': 'Explanation',
                'points_earned': 'Points Earned',
                
                # Study Plan
                'personalized_study_plan': 'Personalized Study Plan',
                'generate_study_plan': 'Generate Study Plan',
                'daily_schedule': 'Daily Schedule',
                'weekly_goals': 'Weekly Goals',
                'recommended_topics': 'Recommended Topics',
                'study_tips': 'Study Tips',
                'time_slot': 'Time Slot',
                'subject': 'Subject',
                'duration': 'Duration',
                'activity': 'Activity',
                'priority': 'Priority',
                
                # Analytics
                'performance_analytics': 'Performance Analytics',
                'overall_performance': 'Overall Performance',
                'topic_wise_performance': 'Topic-wise Performance',
                'recent_activity': 'Recent Activity',
                'performance_trend': 'Performance Trend',
                'weak_topics': 'Topics to Focus On',
                'strong_topics': 'Strong Topics',
                'average_score': 'Average Score',
                'best_score': 'Best Score',
                'total_attempts': 'Total Attempts',
                
                # Mock Interview
                'ai_mock_interview': 'AI Mock Interview',
                'interview_topic': 'Interview Topic',
                'start_interview': 'Start Interview',
                'record_answer': 'Record Your Answer',
                'submit_response': 'Submit Response',
                'interview_feedback': 'Interview Feedback',
                'score': 'Score',
                'strengths': 'Strengths',
                'improvements': 'Areas for Improvement',
                'model_answer': 'Model Answer',
                'overall_feedback': 'Overall Feedback',
                
                # Current Affairs
                'current_affairs_tracker': 'Current Affairs Tracker',
                'latest_updates': 'Latest Updates',
                'generate_questions': 'Generate Questions',
                'news_topic': 'News Topic',
                
                # Common
                'loading': 'Loading...',
                'error': 'Error',
                'success': 'Success',
                'retry': 'Retry',
                'back': 'Back',
                'continue': 'Continue',
                'reset': 'Reset',
                'save': 'Save',
                'cancel': 'Cancel',
                'close': 'Close'
            },
            'hi': {
                # App main
                'app_title': 'एआई सरकारी नौकरी तैयारी',
                'welcome_message': 'एआई-संचालित सरकारी नौकरी तैयारी में आपका स्वागत है',
                'app_description': '🎯 एआई-संचालित क्विज़, व्यक्तिगत अध्ययन योजना और व्यापक विश्लेषण के साथ भारतीय सरकारी परीक्षाओं की तैयारी करें। हमारे बुद्धिमान शिक्षण मंच के साथ यूपीएससी, एसएससी, बैंकिंग, रेलवे और अन्य प्रतियोगी परीक्षाओं में महारत हासिल करें।',
                
                # Navigation
                'home': 'होम',
                'quiz': 'एआई क्विज़',
                'study_plan': 'अध्ययन योजना',
                'analytics': 'विश्लेषण',
                'mock_interview': 'मॉक इंटरव्यू',
                'current_affairs': 'समसामयिकी',
                
                # Profile
                'profile_setup': 'प्रोफाइल सेटअप',
                'your_name': 'आपका नाम',
                'target_exam': 'लक्षित परीक्षा',
                'target_date': 'लक्षित दिनांक',
                'daily_study_hours': 'दैनिक अध्ययन घंटे',
                'save_profile': 'प्रोफाइल सेव करें',
                'profile_saved': 'प्रोफाइल सफलतापूर्वक सेव हो गया!',
                
                # Quick stats
                'quick_stats': 'त्वरित आँकड़े',
                'total_points': 'कुल अंक',
                'study_streak': 'अध्ययन श्रृंखला',
                'days': 'दिन',
                'quizzes_completed': 'पूर्ण क्विज़',
                'achievements': 'उपलब्धियाँ',
                
                # Quick actions
                'quick_actions': 'त्वरित कार्य',
                'take_quiz': 'क्विज़ लें',
                'view_progress': 'प्रगति देखें',
                'mock_interview': 'मॉक इंटरव्यू',
                
                # Quiz
                'quiz_generator': 'एआई क्विज़ जेनरेटर',
                'select_topic': 'विषय चुनें',
                'select_difficulty': 'कठिनाई चुनें (1-5)',
                'number_of_questions': 'प्रश्नों की संख्या',
                'generate_quiz': 'क्विज़ जेनरेट करें',
                'submit_answer': 'उत्तर सबमिट करें',
                'next_question': 'अगला प्रश्न',
                'quiz_completed': 'क्विज़ पूर्ण!',
                'your_score': 'आपका स्कोर',
                'correct_answer': 'सही उत्तर',
                'explanation': 'स्पष्टीकरण',
                'points_earned': 'अर्जित अंक',
                
                # Study Plan
                'personalized_study_plan': 'व्यक्तिगत अध्ययन योजना',
                'generate_study_plan': 'अध्ययन योजना बनाएं',
                'daily_schedule': 'दैनिक कार्यक्रम',
                'weekly_goals': 'साप्ताहिक लक्ष्य',
                'recommended_topics': 'अनुशंसित विषय',
                'study_tips': 'अध्ययन सुझाव',
                'time_slot': 'समय स्लॉट',
                'subject': 'विषय',
                'duration': 'अवधि',
                'activity': 'गतिविधि',
                'priority': 'प्राथमिकता',
                
                # Analytics
                'performance_analytics': 'प्रदर्शन विश्लेषण',
                'overall_performance': 'समग्र प्रदर्शन',
                'topic_wise_performance': 'विषयवार प्रदर्शन',
                'recent_activity': 'हाल की गतिविधि',
                'performance_trend': 'प्रदर्शन प्रवृत्ति',
                'weak_topics': 'सुधार के विषय',
                'strong_topics': 'मजबूत विषय',
                'average_score': 'औसत स्कोर',
                'best_score': 'सर्वश्रेष्ठ स्कोर',
                'total_attempts': 'कुल प्रयास',
                
                # Mock Interview
                'ai_mock_interview': 'एआई मॉक इंटरव्यू',
                'interview_topic': 'इंटरव्यू विषय',
                'start_interview': 'इंटरव्यू शुरू करें',
                'record_answer': 'अपना उत्तर रिकॉर्ड करें',
                'submit_response': 'प्रतिक्रिया सबमिट करें',
                'interview_feedback': 'इंटरव्यू फीडबैक',
                'score': 'स्कोर',
                'strengths': 'शक्तियाँ',
                'improvements': 'सुधार के क्षेत्र',
                'model_answer': 'आदर्श उत्तर',
                'overall_feedback': 'समग्र फीडबैक',
                
                # Current Affairs
                'current_affairs_tracker': 'समसामयिकी ट्रैकर',
                'latest_updates': 'नवीनतम अपडेट',
                'generate_questions': 'प्रश्न जेनरेट करें',
                'news_topic': 'समाचार विषय',
                
                # Common
                'loading': 'लोड हो रहा है...',
                'error': 'त्रुटि',
                'success': 'सफलता',
                'retry': 'पुनः प्रयास',
                'back': 'वापस',
                'continue': 'जारी रखें',
                'reset': 'रीसेट',
                'save': 'सेव करें',
                'cancel': 'रद्द करें',
                'close': 'बंद करें'
            }
        }
    
    def get_text(self, key: str, language: str = 'en') -> str:
        """Get translated text for a given key and language"""
        return self.translations.get(language, {}).get(key, key)
    
    def get_menu_options(self, language: str = 'en') -> Dict[str, str]:
        """Get menu options in the specified language"""
        return {
            self.get_text('home', language): 'home',
            self.get_text('quiz', language): 'quiz',
            self.get_text('study_plan', language): 'study_plan',
            self.get_text('analytics', language): 'analytics',
            self.get_text('mock_interview', language): 'mock_interview',
            self.get_text('current_affairs', language): 'current_affairs'
        }
    
    def get_exam_types(self, language: str = 'en') -> Dict[str, str]:
        """Get exam types in the specified language"""
        if language == 'hi':
            return {
                'UPSC Civil Services': 'यूपीएससी सिविल सेवा',
                'SSC CGL': 'एसएससी सीजीएल',
                'SSC CHSL': 'एसएससी सीएचएसएल',
                'Banking (IBPS/SBI)': 'बैंकिंग (आईबीपीएस/एसबीआई)',
                'Railway (RRB)': 'रेलवे (आरआरबी)',
                'State PSC': 'राज्य पीएससी',
                'Teaching (CTET/TET)': 'शिक्षण (सीटेट/टेट)',
                'Defense (CDS/NDA)': 'रक्षा (सीडीएस/एनडीए)',
                'Police/Constable': 'पुलिस/कांस्टेबल',
                'Other': 'अन्य'
            }
        else:
            return {
                'UPSC Civil Services': 'UPSC Civil Services',
                'SSC CGL': 'SSC Combined Graduate Level',
                'SSC CHSL': 'SSC Combined Higher Secondary Level',
                'Banking (IBPS/SBI)': 'Banking (IBPS/SBI)',
                'Railway (RRB)': 'Railway Recruitment Board',
                'State PSC': 'State Public Service Commission',
                'Teaching (CTET/TET)': 'Teaching (CTET/TET)',
                'Defense (CDS/NDA)': 'Defense (CDS/NDA)',
                'Police/Constable': 'Police/Constable',
                'Other': 'Other'
            }
    
    def get_quiz_topics(self, language: str = 'en') -> Dict[str, str]:
        """Get quiz topics in the specified language"""
        if language == 'hi':
            return {
                'General Knowledge': 'सामान्य ज्ञान',
                'Indian History': 'भारतीय इतिहास',
                'Geography': 'भूगोल',
                'Indian Polity': 'भारतीय राजव्यवस्था',
                'Economics': 'अर्थशास्त्र',
                'Current Affairs': 'समसामयिकी',
                'Science & Technology': 'विज्ञान और प्रौद्योगिकी',
                'Environment': 'पर्यावरण',
                'Mathematics': 'गणित',
                'English': 'अंग्रेजी',
                'Reasoning': 'तर्कशक्ति',
                'Computer Knowledge': 'कंप्यूटर ज्ञान'
            }
        else:
            return {
                'General Knowledge': 'General Knowledge',
                'Indian History': 'Indian History',
                'Geography': 'Geography',
                'Indian Polity': 'Indian Polity & Constitution',
                'Economics': 'Economics',
                'Current Affairs': 'Current Affairs',
                'Science & Technology': 'Science & Technology',
                'Environment': 'Environment & Ecology',
                'Mathematics': 'Mathematics',
                'English': 'English Language',
                'Reasoning': 'Logical Reasoning',
                'Computer Knowledge': 'Computer Knowledge'
            }
    
    def get_interview_topics(self, language: str = 'en') -> Dict[str, str]:
        """Get interview topics in the specified language"""
        if language == 'hi':
            return {
                'Personal Background': 'व्यक्तिगत पृष्ठभूमि',
                'Career Goals': 'करियर लक्ष्य',
                'Current Affairs': 'समसामयिकी',
                'Government Policies': 'सरकारी नीतियां',
                'Social Issues': 'सामाजिक मुद्दे',
                'Leadership': 'नेतृत्व',
                'Problem Solving': 'समस्या समाधान',
                'Ethics': 'नैतिकता',
                'Public Administration': 'लोक प्रशासन'
            }
        else:
            return {
                'Personal Background': 'Personal Background',
                'Career Goals': 'Career Goals & Motivation',
                'Current Affairs': 'Current Affairs',
                'Government Policies': 'Government Policies',
                'Social Issues': 'Social Issues',
                'Leadership': 'Leadership & Management',
                'Problem Solving': 'Problem Solving',
                'Ethics': 'Ethics & Integrity',
                'Public Administration': 'Public Administration'
            }
    
    def get_current_affairs_categories(self, language: str = 'en') -> Dict[str, str]:
        """Get current affairs categories in the specified language"""
        if language == 'hi':
            return {
                'National Politics': 'राष्ट्रीय राजनीति',
                'International Relations': 'अंतर्राष्ट्रीय संबंध',
                'Economy & Business': 'अर्थव्यवस्था और व्यापार',
                'Science & Technology': 'विज्ञान और प्रौद्योगिकी',
                'Sports': 'खेल',
                'Awards & Recognition': 'पुरस्कार और सम्मान',
                'Government Schemes': 'सरकारी योजनाएं',
                'Environment': 'पर्यावरण',
                'Defense': 'रक्षा',
                'Education': 'शिक्षा'
            }
        else:
            return {
                'National Politics': 'National Politics',
                'International Relations': 'International Relations',
                'Economy & Business': 'Economy & Business',
                'Science & Technology': 'Science & Technology',
                'Sports': 'Sports',
                'Awards & Recognition': 'Awards & Recognition',
                'Government Schemes': 'Government Schemes',
                'Environment': 'Environment',
                'Defense': 'Defense',
                'Education': 'Education'
            }
