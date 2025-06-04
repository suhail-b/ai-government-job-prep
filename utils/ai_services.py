import json
import os
from openai import OpenAI
import streamlit as st
from typing import List, Dict, Any
import random

class AIServices:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            st.error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
    
    def generate_quiz_questions(self, topic: str, difficulty: int, language: str = 'en', num_questions: int = 5) -> List[Dict]:
        """Generate quiz questions using OpenAI API"""
        if not self.client:
            return self._get_fallback_questions(topic, difficulty, language, num_questions)
        
        try:
            lang_instruction = "in Hindi (Devanagari script)" if language == 'hi' else "in English"
            
            prompt = f"""Generate {num_questions} multiple choice questions for Indian government job preparation exams 
            on the topic "{topic}" with difficulty level {difficulty}/5 (1=beginner, 5=expert) {lang_instruction}.
            
            Focus on topics relevant to Indian government exams like UPSC, SSC, Banking, Railways, etc.
            
            Return the response as a JSON object with this exact structure:
            {{
                "questions": [
                    {{
                        "question": "Question text here",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": 0,
                        "explanation": "Detailed explanation of the correct answer",
                        "difficulty": {difficulty},
                        "topic": "{topic}"
                    }}
                ]
            }}
            
            Make sure all content is culturally appropriate for Indian government exam preparation.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                messages=[
                    {"role": "system", "content": "You are an expert in Indian government job preparation and exam content creation."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("questions", [])
            
        except Exception as e:
            st.error(f"Error generating quiz questions: {str(e)}")
            return self._get_fallback_questions(topic, difficulty, language, num_questions)
    
    def generate_study_plan(self, user_data: Dict, language: str = 'en') -> Dict:
        """Generate personalized study plan using AI"""
        if not self.client:
            return self._get_fallback_study_plan(user_data, language)
        
        try:
            lang_instruction = "in Hindi (Devanagari script)" if language == 'hi' else "in English"
            
            prompt = f"""Create a personalized study plan for Indian government job exam preparation {lang_instruction}.
            
            User Profile:
            - Target Exam: {user_data.get('exam_type', 'General')}
            - Daily Study Hours: {user_data.get('study_hours_per_day', 2)}
            - Current Performance: {len(user_data.get('quiz_scores', []))} quizzes completed
            - Average Score: {sum(user_data.get('quiz_scores', [0]))/max(len(user_data.get('quiz_scores', [1])), 1):.1f}%
            
            Return a JSON object with this structure:
            {{
                "daily_schedule": [
                    {{
                        "time_slot": "Morning/Afternoon/Evening",
                        "subject": "Subject name",
                        "duration": "Duration in minutes",
                        "activity": "Specific activity",
                        "priority": "High/Medium/Low"
                    }}
                ],
                "weekly_goals": [
                    "Goal 1",
                    "Goal 2",
                    "Goal 3"
                ],
                "recommended_topics": [
                    "Topic 1",
                    "Topic 2",
                    "Topic 3"
                ],
                "study_tips": [
                    "Tip 1",
                    "Tip 2",
                    "Tip 3"
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                messages=[
                    {"role": "system", "content": "You are an expert study planner for Indian government job preparation."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            st.error(f"Error generating study plan: {str(e)}")
            return self._get_fallback_study_plan(user_data, language)
    
    def conduct_mock_interview(self, question: str, user_answer: str, language: str = 'en') -> Dict:
        """Evaluate mock interview responses"""
        if not self.client:
            return self._get_fallback_interview_feedback(question, user_answer, language)
        
        try:
            lang_instruction = "in Hindi (Devanagari script)" if language == 'hi' else "in English"
            
            prompt = f"""Evaluate this mock interview response for Indian government job interview {lang_instruction}.
            
            Question: {question}
            Candidate's Answer: {user_answer}
            
            Provide detailed feedback as JSON:
            {{
                "score": 85,
                "strengths": ["Point 1", "Point 2"],
                "improvements": ["Area 1", "Area 2"],
                "model_answer": "A better way to answer this question would be...",
                "overall_feedback": "Overall assessment of the response"
            }}
            
            Score should be out of 100. Focus on Indian government service context.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                messages=[
                    {"role": "system", "content": "You are an expert interviewer for Indian government job positions."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.6
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            st.error(f"Error evaluating interview response: {str(e)}")
            return self._get_fallback_interview_feedback(question, user_answer, language)
    
    def generate_current_affairs_questions(self, topic: str, language: str = 'en') -> List[Dict]:
        """Generate current affairs questions"""
        if not self.client:
            return []
        
        try:
            lang_instruction = "in Hindi (Devanagari script)" if language == 'hi' else "in English"
            
            prompt = f"""Generate 3 current affairs questions related to "{topic}" for Indian government job exams {lang_instruction}.
            
            Focus on recent developments in Indian politics, economy, international relations, science & technology,
            sports, awards, and government schemes that are relevant for competitive exams.
            
            Return JSON format:
            {{
                "questions": [
                    {{
                        "question": "Question text",
                        "options": ["A", "B", "C", "D"],
                        "correct_answer": 0,
                        "explanation": "Why this is correct and current",
                        "date_relevance": "Month Year or recent timeframe"
                    }}
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                messages=[
                    {"role": "system", "content": "You are an expert in Indian current affairs and government exam preparation."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("questions", [])
            
        except Exception as e:
            st.error(f"Error generating current affairs questions: {str(e)}")
            return []
    
    def _get_fallback_questions(self, topic: str, difficulty: int, language: str, num_questions: int) -> List[Dict]:
        """Fallback questions when API is not available"""
        return []
    
    def _get_fallback_study_plan(self, user_data: Dict, language: str) -> Dict:
        """Fallback study plan when API is not available"""
        if language == 'hi':
            return {
                "daily_schedule": [
                    {
                        "time_slot": "सुबह",
                        "subject": "सामान्य ज्ञान",
                        "duration": "60 मिनट",
                        "activity": "पुस्तक अध्ययन",
                        "priority": "उच्च"
                    }
                ],
                "weekly_goals": ["दैनिक अभ्यास", "मॉक टेस्ट", "करंट अफेयर्स"],
                "recommended_topics": ["भारतीय इतिहास", "भूगोल", "राजनीति"],
                "study_tips": ["नियमित अभ्यास करें", "नोट्स बनाएं", "रिवीजन करें"]
            }
        else:
            return {
                "daily_schedule": [
                    {
                        "time_slot": "Morning",
                        "subject": "General Knowledge",
                        "duration": "60 minutes",
                        "activity": "Book Reading",
                        "priority": "High"
                    }
                ],
                "weekly_goals": ["Daily Practice", "Mock Tests", "Current Affairs"],
                "recommended_topics": ["Indian History", "Geography", "Polity"],
                "study_tips": ["Practice regularly", "Make notes", "Regular revision"]
            }
    
    def _get_fallback_interview_feedback(self, question: str, answer: str, language: str) -> Dict:
        """Fallback interview feedback when API is not available"""
        if language == 'hi':
            return {
                "score": 75,
                "strengths": ["अच्छी समझ", "स्पष्ट उत्तर"],
                "improvements": ["और विस्तार से बताएं", "उदाहरण दें"],
                "model_answer": "इस प्रश्न का बेहतर उत्तर होगा...",
                "overall_feedback": "अच्छी कोशिश, और सुधार की गुंजाइश है"
            }
        else:
            return {
                "score": 75,
                "strengths": ["Good understanding", "Clear response"],
                "improvements": ["Provide more details", "Add examples"],
                "model_answer": "A better answer would be...",
                "overall_feedback": "Good attempt, room for improvement"
            }
