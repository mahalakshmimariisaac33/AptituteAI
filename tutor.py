"""
Tutor Agent to explain solutions step-by-step
"""

import ollama
from typing import Dict


class TutorAgent:
    def __init__(self, model: str = "llama3"):
        """
        Initialize the tutor agent with Ollama model
        """
        self.model = model
    
    def explain_solution(
        self, 
        question: str, 
        user_answer: str, 
        correct_answer: str,
        explanation: str
    ) -> Dict[str, str]:
        """
        Provide a detailed step-by-step explanation of the solution
        
        Args:
            question: The question text
            user_answer: User's submitted answer
            correct_answer: The correct answer
            explanation: Basic explanation from question generator
            
        Returns:
            Dictionary with detailed explanation and tips
        """
        try:
            prompt = f"""Question: {question}
User's Answer: {user_answer}
Correct Answer: {correct_answer}
Basic Explanation: {explanation}

Provide a detailed, step-by-step explanation that:
1. Is easy to understand for a student
2. Breaks down the problem into simple steps
3. Uses clear language
4. Includes any shortcuts or tricks
5. Encourages the student

Format your response as:
DETAILED_EXPLANATION: [Your step-by-step explanation]
SHORTCUT_TIP: [Any shortcut or trick if applicable]
ENCOURAGEMENT: [A brief encouraging message]"""
            
            response = ollama.chat(model=self.model, messages=[
                {
                    'role': 'system',
                    'content': 'You are a friendly and patient tutor. Explain concepts clearly and simply.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ])
            
            return self._parse_tutor_response(response['message']['content'])
            
        except Exception as e:
            print(f"Error in tutor explanation: {e}")
            # Return fallback explanation
            return {
                "detailed_explanation": explanation,
                "shortcut_tip": "Practice similar problems to build speed and accuracy.",
                "encouragement": "Keep practicing! You're improving every day."
            }
    
    def _parse_tutor_response(self, response: str) -> Dict[str, str]:
        """Parse the tutor response"""
        
        detailed_explanation = ""
        shortcut_tip = ""
        encouragement = ""
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith("DETAILED_EXPLANATION:"):
                current_section = "detailed"
                detailed_explanation = line.replace("DETAILED_EXPLANATION:", "").strip()
            elif line.startswith("SHORTCUT_TIP:"):
                current_section = "shortcut"
                shortcut_tip = line.replace("SHORTCUT_TIP:", "").strip()
            elif line.startswith("ENCOURAGEMENT:"):
                current_section = "encouragement"
                encouragement = line.replace("ENCOURAGEMENT:", "").strip()
            elif current_section:
                if current_section == "detailed":
                    detailed_explanation += " " + line
                elif current_section == "shortcut":
                    shortcut_tip += " " + line
                elif current_section == "encouragement":
                    encouragement += " " + line
        
        return {
            "detailed_explanation": detailed_explanation.strip() or "Solution explained step by step.",
            "shortcut_tip": shortcut_tip.strip() or "Practice regularly to improve!",
            "encouragement": encouragement.strip() or "You're doing great!"
        }
