from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re
import time

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise Exception("❌ OPENROUTER_API_KEY not found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def generate_ai_question(topic, difficulty):

    seed = int(time.time() * 1000) % 100000

    prompt = f"""
You are an expert aptitude question generator.

TASK:
Generate ONE high-quality aptitude question based on standard competitive exam syllabus.

STRICT RULES:
- Must be REAL aptitude concepts (no fake company exam questions)
- Must NOT mention any company (no Google, Amazon, TCS references)
- Must be logically correct and solvable
- Must be unique every time
- Must follow standard topics: Quantitative, Logical Reasoning, Verbal Ability
- Must NOT copy any known previous question directly
- Must include proper solution steps

Unique Seed: {seed}

Topic: {topic}
Difficulty: {difficulty}

Return ONLY valid JSON:

{{
    "sub_topic": "",
    "question": "",
    "options": [
        "A) ",
        "B) ",
        "C) ",
        "D) "
    ],
    "correct_answer": "A",
    "solution_steps": ""
}}
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=1.0
        )

        content = response.choices[0].message.content
        content = re.sub(r"```json|```", "", content).strip()

        return json.loads(content)

    except Exception as e:
        print("❌ AI GENERATION FAILED:", str(e))
        raise Exception("AI failed to generate question. Check API / model / key.")