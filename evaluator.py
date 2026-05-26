"""
Evaluator Agent to check user answers and provide feedback
"""

import ollama
from typing import Dict, Tuple
import re


class AnswerEvaluator:
    def __init__(self, model: str = "mistral"):
        """
        Initialize the answer evaluator with Ollama model
        """
        self.model = model
    
    def evaluate_answer(
        self, 
        question: str, 
        user_answer: str, 
        correct_answer: str
    ) -> Tuple[bool, str]:
        """
        Evaluate the user's answer against the correct answer
        
        Args:
            question: The question text
            user_answer: User's submitted answer
            correct_answer: The correct answer
            
        Returns:
            Tuple of (is_correct, feedback_message)
        """
        # Extract option letter if present (e.g., "A", "B", "C", "D")
        user_option = self._extract_option_letter(user_answer)
        correct_option = self._extract_option_letter(correct_answer)
        
        # If both have option letters, compare them
        if user_option and correct_option:
            if user_option.upper() == correct_option.upper():
                return True, "Perfect! Your answer is correct."
            else:
                return False, f"Incorrect. The correct answer is {correct_answer}"
        
        # Normalize answers for comparison
        user_normalized = self._normalize_answer(user_answer)
        correct_normalized = self._normalize_answer(correct_answer)
        
        # Direct match check
        if user_normalized == correct_normalized:
            return True, "Perfect! Your answer is correct."
        
        # Use LLM for intelligent evaluation
        try:
            prompt = f"""Question: {question}
Correct Answer: {correct_answer}
User Answer: {user_answer}

Evaluate if the user's answer is correct. Consider:
- Numerical answers should match exactly
- Multiple choice selections should match (A, B, C, D)
- Word answers can have slight variations
- Partial credit for close answers

Respond with either:
CORRECT: [reasoning]
INCORRECT: [reasoning]"""
            
            response = ollama.chat(model=self.model, messages=[
                {
                    'role': 'system',
                    'content': 'You are an expert answer evaluator. Be fair but accurate.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ])
            
            result = response['message']['content']
            
            if "CORRECT" in result.upper():
                return True, result.split("CORRECT:")[-1].strip()
            else:
                return False, result.split("INCORRECT:")[-1].strip()
                
        except Exception as e:
            print(f"Error in LLM evaluation: {e}")
            # Fallback to simple comparison
            similarity = self._calculate_similarity(user_normalized, correct_normalized)
            
            if similarity > 0.8:
                return True, "Your answer is correct!"
            elif similarity > 0.5:
                return False, f"Close! The correct answer is: {correct_answer}"
            else:
                return False, f"Incorrect. The correct answer is: {correct_answer}"
    
    def _extract_option_letter(self, answer: str) -> str:
        """Extract option letter (A, B, C, D) from answer"""
        import re
        # Match patterns like "A", "A)", "A) 120", etc.
        match = re.match(r'^([A-D])[)\s]', answer.strip().upper())
        if match:
            return match.group(1)
        # Check if answer is just a single letter
        if len(answer.strip()) == 1 and answer.strip().upper() in ['A', 'B', 'C', 'D']:
            return answer.strip().upper()
        return ""
    
    def _normalize_answer(self, answer: str) -> str:
        """Normalize answer for comparison"""
        # Remove extra whitespace
        answer = " ".join(answer.split())
        # Convert to lowercase
        answer = answer.lower()
        # Remove common punctuation
        answer = re.sub(r'[.,;:!?()"\']', '', answer)
        # Extract numbers
        numbers = re.findall(r'\d+', answer)
        if numbers and len(numbers) == 1:
            return numbers[0]
        return answer
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate simple similarity between two strings"""
        if str1 == str2:
            return 1.0
        
        # Check if one is substring of other
        if str1 in str2 or str2 in str1:
            return 0.8
        
        # Check for common words
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
