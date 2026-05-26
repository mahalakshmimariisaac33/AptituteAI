"""
Motivation System for encouraging users
"""

import random
from typing import List


class MotivationSystem:
    def __init__(self):
        """
        Initialize the motivation system
        """
        self.correct_answers = [
            "🎉 Amazing work!",
            "🔥 Excellent improvement!",
            "🚀 You're getting smarter!",
            "🧠 Brilliant thinking!",
            "👏 Keep practicing!",
            "⚡ Fast learner!",
            "🌟 Outstanding!",
            "💪 Strong work!",
            "🎯 Perfect aim!",
            "✨ You're on fire!",
            "🏆 Champion mindset!",
            "💎 Diamond quality!",
            "🌈 Rainbow performance!",
            "⭐ Star quality!",
            "🦅 Eagle eye!"
        ]
        
        self.incorrect_answers = [
            "💪 Don't give up!",
            "🌱 Every mistake is a lesson!",
            "📚 Keep learning!",
            "🎯 Practice makes perfect!",
            "💡 You're getting closer!",
            "🔄 Try again, you've got this!",
            "🌟 Stay positive!",
            "🚀 Keep pushing forward!",
            "🧩 Piece by piece!",
            "📈 Progress takes time!",
            "💎 Effort counts!",
            "🌻 Grow from this!",
            "🎨 Learning is art!",
            "🔑 Unlock your potential!",
            "⚡ Charge ahead!"
        ]
        
        self.streak_messages = [
            "🔥 You're on a roll!",
            "⚡ Unstoppable streak!",
            "🚀 Rocketing to success!",
            "💫 Shining bright!",
            "🌟 Star performance!",
            "🏆 Winning streak!",
            "🎪 Showtime!",
            "🎪 Amazing momentum!"
        ]
        
        self.badge_messages = [
            "🎊 Congratulations on earning a new badge!",
            "🏅 Badge unlocked! You're making progress!",
            "🌟 Achievement unlocked!",
            "🎉 New badge added to your collection!",
            "🏆 You've earned a new achievement!",
            "⭐ Badge acquired! Keep it up!",
            "🎪 Badge celebration time!",
            "🌈 New badge, new motivation!"
        ]
    
    def get_motivation(self, is_correct: bool, streak: int = 0) -> str:
        """
        Get a motivational message based on performance
        
        Args:
            is_correct: Whether the answer was correct
            streak: Current streak of correct answers
            
        Returns:
            Motivational message
        """
        if streak >= 3:
            return random.choice(self.streak_messages)
        
        if is_correct:
            return random.choice(self.correct_answers)
        else:
            return random.choice(self.incorrect_answers)
    
    def get_badge_motivation(self) -> str:
        """Get a motivational message for earning a badge"""
        return random.choice(self.badge_messages)
    
    def get_session_start_motivation(self) -> str:
        """Get a motivational message for starting a session"""
        messages = [
            "🎯 Ready to ace some questions?",
            "🚀 Let's start learning!",
            "💪 You've got this!",
            "🌟 Time to shine!",
            "🧠 Exercise your brain!",
            "⚡ Let's go!",
            "🎪 Show your skills!",
            "📚 Knowledge time!"
        ]
        return random.choice(messages)
    
    def get_difficulty_motivation(self, difficulty: str, increased: bool) -> str:
        """
        Get a motivational message for difficulty change
        
        Args:
            difficulty: New difficulty level
            increased: Whether difficulty was increased
            
        Returns:
            Motivational message
        """
        if increased:
            messages = {
                "Easy": "🌱 Starting easy to build confidence!",
                "Medium": "⚡ Leveling up to Medium!",
                "Hard": "🔥 Challenging yourself with Hard!"
            }
        else:
            messages = {
                "Easy": "🌱 Let's build up with easier questions!",
                "Medium": "📈 Perfect time for Medium level!",
                "Hard": "💪 You're ready for a challenge!"
            }
        
        return messages.get(difficulty, "🎯 Keep pushing!")
