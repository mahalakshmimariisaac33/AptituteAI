"""
Expert Aptitude Question Generator AI for Top Company Placements
Generates UNIQUE, high-quality aptitude questions for TCS, Infosys, Amazon, Google
"""

import ollama
import json
import uuid
import random
from typing import Dict
from vector_db import QuestionVectorDB


class QuestionGenerator:

    def __init__(self, model: str = "llama3"):

        self.model = model

        # Company-level mapping
        self.company_levels = {
            "Easy": "TCS",
            "Medium": "Infosys", 
            "Hard": "Amazon"
        }

        # Comprehensive topic mapping
        self.topics = {
            "Quantitative Aptitude": [
                "Arithmetic", "Profit & Loss", "Time & Work", 
                "Speed & Distance", "Algebra", "Number System",
                "Probability", "Permutation & Combination"
            ],
            "Logical Reasoning": [
                "Puzzles", "Blood Relations", "Coding-Decoding",
                "Direction Sense", "Seating Arrangement", "Syllogism"
            ],
            "Data Interpretation": [
                "Tables", "Bar Charts", "Line Graphs", "Pie Charts"
            ],
            "Verbal Ability": [
                "Reading Comprehension", "Grammar", "Vocabulary"
            ]
        }

        # Initialize Vector Database
        self.vector_db = QuestionVectorDB()

    # ====================================
    # GENERATE UNIQUE APTITUDE QUESTION
    # ====================================
    def generate_question(
        self,
        category: str = None,
        difficulty: str = "Medium"
    ) -> Dict:

        # Auto-select category if not provided
        if not category:
            import random
            category = random.choice(list(self.topics.keys()))

        # Get sub-topic
        sub_topic = self._get_random_subtopic(category)
        
        # Company level mapping
        company_level = self.company_levels.get(difficulty, "Google")
        if difficulty == "Hard":
            company_level = random.choice(["Amazon", "Google"])

        # Retry generation for uniqueness
        for attempt in range(15):

            # Get previous questions for context
            old_questions = self.vector_db.get_similar_questions(category)

            # Build enhanced prompt
            prompt = self._build_expert_prompt(
                category,
                sub_topic,
                difficulty,
                company_level,
                old_questions,
                attempt
            )

            try:
                response = ollama.chat(
                    model=self.model,
                    messages=[
                        {
                            'role': 'system',
                            'content': self._get_system_prompt()
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    options={
                        "temperature": 1.2 + (attempt * 0.1),  # Increase randomness with attempts
                        "top_p": 0.9,
                        "num_predict": 800
                    }
                )

                # Parse response to JSON
                raw_response = response['message']['content']
                question_data = self._parse_to_json(
                    raw_response, 
                    category, 
                    sub_topic, 
                    difficulty, 
                    company_level
                )

                if not question_data:
                    continue

                question_text = question_data["question"]

                # Strict uniqueness check
                if not self.vector_db.is_similar(question_text, threshold=0.45):
                    
                    # Save to vector database
                    self.vector_db.add_question(question_text, category)
                    
                    return question_data

            except Exception as e:
                print(f"Generation Error (Attempt {attempt + 1}): {e}")
                continue

        # Enhanced fallback with variety
        return self._generate_enhanced_fallback(category, sub_topic, difficulty, company_level)

    # ====================================
    # SYSTEM PROMPT FOR EXPERT GENERATION
    # ====================================
    def _get_system_prompt(self) -> str:
        return """You are an expert Aptitude Question Generator AI designed to train students for top company placements such as TCS, Infosys, Amazon, and Google.

🎯 CORE MISSION:
- Generate ONE unique, high-quality aptitude question per request
- Train users for real placement exams with company-level difficulty
- Ensure questions are realistic and interview-level
- Improve logical thinking and problem-solving skills

🚫 STRICT UNIQUENESS RULES:
- Do NOT repeat any question (even slightly modified versions)
- Do NOT reuse same numbers or patterns  
- Every question must be logically unique
- Avoid template-based questions
- Create fresh, original problems every time

🎚 DIFFICULTY STANDARDS:
Easy (TCS Level): Direct formula-based, 1-step solution
Medium (Infosys Level): Multi-step reasoning, mix of concepts  
Hard (Amazon/Google Level): Logical traps, complex reasoning, interview-level thinking

📋 OUTPUT REQUIREMENT:
Return ONLY valid JSON format. No explanation text outside JSON.

Be creative, challenging, and ensure every question tests real aptitude skills needed for placements."""
    # ====================================
    # BUILD EXPERT GENERATION PROMPT
    # ====================================
    def _build_expert_prompt(
        self,
        category: str,
        sub_topic: str,
        difficulty: str,
        company_level: str,
        old_questions: list,
        attempt: int
    ) -> str:

        # Memory context to avoid repetition
        memory_context = ""
        if old_questions:
            memory_context = "\n🚫 DO NOT REPEAT THESE PATTERNS:\n"
            for q in old_questions[-8:]:  # Show more context
                memory_context += f"- {q[:100]}...\n"

        # Difficulty-specific guidelines
        difficulty_guide = {
            "Easy": """
🟢 EASY (TCS Level):
- Basic arithmetic or simple logic
- Direct formula application
- One-step solution
- Clear, straightforward approach
""",
            "Medium": """  
🟡 MEDIUM (Infosys Level):
- Moderate calculations with 2-3 steps
- Combine multiple concepts
- Requires logical reasoning
- Slightly tricky but solvable
""",
            "Hard": """
🔴 HARD (Amazon/Google Level):
- Complex multi-layered logic
- Puzzle-based or pattern recognition
- Multiple solution approaches possible
- Interview-level challenge
- May include logical traps
"""
        }

        # Creativity boosters based on attempt
        creativity_boost = ""
        if attempt > 5:
            creativity_boost = f"""
🎨 CREATIVITY BOOST (Attempt {attempt + 1}):
- Use unusual number combinations
- Try different question structures  
- Explore edge cases or special scenarios
- Think outside conventional patterns
"""

        prompt = f"""
Generate ONE completely unique aptitude question.

📚 CATEGORY: {category}
🎯 SUB-TOPIC: {sub_topic}  
🎚 DIFFICULTY: {difficulty}
🏢 COMPANY LEVEL: {company_level}

{difficulty_guide.get(difficulty, "")}

{memory_context}

{creativity_boost}

🎯 REQUIREMENTS:
- Must be completely different from previous questions
- Use fresh numbers, logic, and wording
- Realistic placement exam style
- Test genuine problem-solving skills
- Include logical distractors in options

📋 STRICT JSON OUTPUT FORMAT:
```json
{{
    "id": "unique_question_id",
    "company_level": "{company_level}",
    "topic": "{category}",
    "sub_topic": "{sub_topic}",
    "difficulty": "{difficulty}",
    "question": "The complete aptitude question here",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "A",
    "solution_steps": "Step-by-step explanation of the solution",
    "concept_used": ["concept1", "concept2"]
}}
```

Generate the JSON now:"""

        return prompt

    # ====================================
    # PARSE RESPONSE TO JSON FORMAT
    # ====================================
    def _parse_to_json(
        self,
        response: str,
        category: str,
        sub_topic: str,
        difficulty: str,
        company_level: str
    ) -> Dict:

        try:
            # Try to extract JSON from response
            import re
            
            # Look for JSON block
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON without code blocks
                json_match = re.search(r'(\{.*?\})', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    return None

            # Parse JSON
            question_data = json.loads(json_str)
            
            # Validate required fields
            required_fields = ["question", "options", "correct_answer", "solution_steps"]
            for field in required_fields:
                if field not in question_data or not question_data[field]:
                    return None

            # Ensure proper format
            question_data["id"] = question_data.get("id", str(uuid.uuid4())[:8])
            question_data["company_level"] = company_level
            question_data["topic"] = category
            question_data["sub_topic"] = sub_topic
            question_data["difficulty"] = difficulty
            
            # Ensure options is a list
            if isinstance(question_data["options"], str):
                # Convert string options to list
                options_text = question_data["options"]
                options_list = []
                for line in options_text.split('\n'):
                    line = line.strip()
                    if line and (line.startswith('A)') or line.startswith('B)') or 
                               line.startswith('C)') or line.startswith('D)')):
                        options_list.append(line)
                question_data["options"] = options_list

            # Validate options format
            if len(question_data["options"]) != 4:
                return None

            # Ensure concept_used is a list
            if "concept_used" not in question_data:
                question_data["concept_used"] = [sub_topic]
            elif isinstance(question_data["concept_used"], str):
                question_data["concept_used"] = [question_data["concept_used"]]

            return question_data

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"JSON parsing error: {e}")
            return None

    # ====================================
    # HELPER METHODS
    # ====================================
    def _get_random_subtopic(self, category: str) -> str:
        """Get a random subtopic for the given category"""
        import random
        subtopics = self.topics.get(category, [category])
        return random.choice(subtopics)

    # ====================================
    # ENHANCED FALLBACK GENERATOR
    # ====================================
    def _generate_enhanced_fallback(
        self,
        category: str,
        sub_topic: str,
        difficulty: str,
        company_level: str
    ) -> Dict:
        """Generate a fallback question when AI generation fails"""
        
        import random
        
        fallback_questions = {
            "Quantitative Aptitude": {
                "Easy": {
                    "question": "A shopkeeper sells an item for ₹450 and makes a profit of 25%. What was the cost price?",
                    "options": ["A) ₹360", "B) ₹375", "C) ₹400", "D) ₹425"],
                    "correct_answer": "A",
                    "solution_steps": "Let CP = x. Then SP = x + 25% of x = 1.25x = 450. So x = 450/1.25 = ₹360",
                    "concept_used": ["Profit & Loss", "Percentage"]
                },
                "Medium": {
                    "question": "Two pipes A and B can fill a tank in 12 hours and 18 hours respectively. If both pipes are opened together, how long will it take to fill the tank?",
                    "options": ["A) 6.5 hours", "B) 7.2 hours", "C) 8.4 hours", "D) 9.6 hours"],
                    "correct_answer": "B",
                    "solution_steps": "Rate of A = 1/12, Rate of B = 1/18. Combined rate = 1/12 + 1/18 = 5/36. Time = 36/5 = 7.2 hours",
                    "concept_used": ["Time & Work", "Fractions"]
                },
                "Hard": {
                    "question": "In how many ways can 5 boys and 3 girls be arranged in a row such that no two girls sit together?",
                    "options": ["A) 14400", "B) 28800", "C) 43200", "D) 57600"],
                    "correct_answer": "A",
                    "solution_steps": "First arrange 5 boys in 5! ways. This creates 6 gaps. Choose 3 gaps for girls in C(6,3) ways and arrange girls in 3! ways. Total = 5! × C(6,3) × 3! = 120 × 20 × 6 = 14400",
                    "concept_used": ["Permutation & Combination", "Arrangement"]
                }
            },
            "Logical Reasoning": {
                "Easy": {
                    "question": "If CODING is written as DPEJOH, how is FLOWER written?",
                    "options": ["A) GMPXFS", "B) GMPWER", "C) GKNVDQ", "D) GMPXFR"],
                    "correct_answer": "A",
                    "solution_steps": "Each letter is shifted by +1 position. F→G, L→M, O→P, W→X, E→F, R→S",
                    "concept_used": ["Coding-Decoding", "Pattern Recognition"]
                }
            }
        }
        
        # Get fallback for category and difficulty
        fallback_data = fallback_questions.get(category, {}).get(difficulty)
        
        if not fallback_data:
            # Default fallback
            fallback_data = fallback_questions["Quantitative Aptitude"]["Easy"]
        
        return {
            "id": str(uuid.uuid4())[:8],
            "company_level": company_level,
            "topic": category,
            "sub_topic": sub_topic,
            "difficulty": difficulty,
            **fallback_data
        }