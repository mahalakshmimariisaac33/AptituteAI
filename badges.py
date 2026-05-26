"""
Badge System for tracking user achievements
"""

from typing import Dict, List
import json
import os


class BadgeSystem:
    def __init__(self):
        """
        Initialize the badge system
        """

        self.badges = {
            "Rising Star": {
                "emoji": "🏅",
                "description": "Answer 5 questions correctly",
                "condition": lambda stats: stats['correct_answers'] >= 5
            },

            "Aptitude Master": {
                "emoji": "🧠",
                "description": "Answer 20 questions correctly",
                "condition": lambda stats: stats['correct_answers'] >= 20
            },

            "Speed Solver": {
                "emoji": "⚡",
                "description": "Answer 3 questions correctly in a row",
                "condition": lambda stats: stats['streak'] >= 3
            },

            "Smart Thinker": {
                "emoji": "🎯",
                "description": "Achieve 80% accuracy with at least 10 questions",
                "condition": lambda stats:
                    stats['total_questions'] >= 10 and
                    stats['accuracy'] >= 80
            },

            "Consistent Learner": {
                "emoji": "🚀",
                "description": "Practice for 5 different sessions",
                "condition": lambda stats: stats['sessions'] >= 5
            },

            "Problem Crusher": {
                "emoji": "🔥",
                "description": "Answer 50 questions total",
                "condition": lambda stats: stats['total_questions'] >= 50
            },

            "Perfect Score": {
                "emoji": "💯",
                "description": "Get 100% accuracy in a session (min 5 questions)",
                "condition": lambda stats:
                    stats['session_correct'] >= 5 and
                    stats['session_accuracy'] == 100
            },

            "Quick Learner": {
                "emoji": "📚",
                "description": "Practice all categories",
                "condition": lambda stats:
                    len(stats['categories_attempted']) >= 4
            }
        }

        self.earned_badges = []
        self.stats_file = "user_stats.json"
        self.user_stats = self._load_stats()

    def _load_stats(self) -> Dict:
        """
        Load user statistics from file
        """

        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:

                    stats = json.load(f)

                    # Convert list back to set
                    stats['categories_attempted'] = set(
                        stats.get('categories_attempted', [])
                    )

                    return stats

            except Exception as e:
                print(f"Error loading stats: {e}")

        return {
            'correct_answers': 0,
            'total_questions': 0,
            'streak': 0,
            'max_streak': 0,
            'sessions': 0,
            'categories_attempted': set(),
            'session_correct': 0,
            'session_total': 0
        }

    def _save_stats(self):
        """
        Save user statistics to file
        """

        stats_to_save = self.user_stats.copy()

        # Convert set → list for JSON
        stats_to_save['categories_attempted'] = list(
            self.user_stats['categories_attempted']
        )

        try:
            with open(self.stats_file, 'w') as f:
                json.dump(stats_to_save, f)

        except Exception as e:
            print(f"Error saving stats: {e}")

    def update_stats(self, is_correct: bool, category: str):
        """
        Update stats after answering a question
        """

        self.user_stats['total_questions'] += 1
        self.user_stats['session_total'] += 1

        # Add category safely
        self.user_stats['categories_attempted'].add(category)

        if is_correct:

            self.user_stats['correct_answers'] += 1
            self.user_stats['session_correct'] += 1
            self.user_stats['streak'] += 1

            if self.user_stats['streak'] > self.user_stats['max_streak']:
                self.user_stats['max_streak'] = self.user_stats['streak']

        else:
            self.user_stats['streak'] = 0

        self._save_stats()

    def start_new_session(self):
        """
        Start new practice session
        """

        self.user_stats['sessions'] += 1
        self.user_stats['session_correct'] = 0
        self.user_stats['session_total'] = 0

        self._save_stats()

    def get_accuracy(self) -> float:
        """
        Calculate overall accuracy
        """

        if self.user_stats['total_questions'] == 0:
            return 0.0

        return (
            self.user_stats['correct_answers']
            / self.user_stats['total_questions']
        ) * 100

    def get_session_accuracy(self) -> float:
        """
        Calculate session accuracy
        """

        if self.user_stats['session_total'] == 0:
            return 0.0

        return (
            self.user_stats['session_correct']
            / self.user_stats['session_total']
        ) * 100

    def check_badges(self) -> List[str]:
        """
        Check newly earned badges
        """

        new_badges = []

        stats = {
            'correct_answers': self.user_stats['correct_answers'],
            'total_questions': self.user_stats['total_questions'],
            'streak': self.user_stats['streak'],
            'accuracy': self.get_accuracy(),
            'sessions': self.user_stats['sessions'],
            'categories_attempted': self.user_stats['categories_attempted'],
            'session_correct': self.user_stats['session_correct'],
            'session_accuracy': self.get_session_accuracy()
        }

        for badge_name, badge_info in self.badges.items():

            if badge_name not in self.earned_badges:

                try:
                    if badge_info['condition'](stats):

                        self.earned_badges.append(badge_name)
                        new_badges.append(badge_name)

                except Exception as e:
                    print(f"Error checking badge {badge_name}: {e}")

        return new_badges

    def get_badge_info(self, badge_name: str) -> Dict:
        """
        Get badge details
        """

        return self.badges.get(badge_name, {})

    def get_all_badges(self) -> Dict:
        """
        Get all badges
        """

        return {
            name: {
                **info,
                'earned': name in self.earned_badges
            }

            for name, info in self.badges.items()
        }

    def get_earned_badges(self) -> List[Dict]:
        """
        Get earned badges
        """

        return [
            {
                'name': name,
                **self.badges[name]
            }

            for name in self.earned_badges
        ]

    def get_stats_summary(self) -> Dict:
        """
        Get user statistics summary
        """

        return {
            'total_questions': self.user_stats['total_questions'],
            'correct_answers': self.user_stats['correct_answers'],
            'accuracy': round(self.get_accuracy(), 1),
            'current_streak': self.user_stats['streak'],
            'max_streak': self.user_stats['max_streak'],
            'sessions': self.user_stats['sessions'],
            'badges_earned': len(self.earned_badges)
        }