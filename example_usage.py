#!/usr/bin/env python3
"""
Example Usage of Enhanced Aptitude Question Generator
Demonstrates how to generate questions for different company levels
"""

from question_generator import QuestionGenerator
import json

def demonstrate_company_levels():
    """Show questions for different company difficulty levels"""
    
    generator = QuestionGenerator()
    
    print("🏢 COMPANY-LEVEL APTITUDE QUESTIONS")
    print("=" * 60)
    
    # TCS Level (Easy)
    print("\n🟢 TCS LEVEL (Easy)")
    print("-" * 30)
    tcs_question = generator.generate_question("Quantitative Aptitude", "Easy")
    print(f"Question: {tcs_question['question']}")
    print(f"Company: {tcs_question['company_level']}")
    print(f"Topic: {tcs_question['sub_topic']}")
    
    # Infosys Level (Medium)  
    print("\n🟡 INFOSYS LEVEL (Medium)")
    print("-" * 30)
    infosys_question = generator.generate_question("Logical Reasoning", "Medium")
    print(f"Question: {infosys_question['question']}")
    print(f"Company: {infosys_question['company_level']}")
    print(f"Topic: {infosys_question['sub_topic']}")
    
    # Amazon/Google Level (Hard)
    print("\n🔴 AMAZON/GOOGLE LEVEL (Hard)")
    print("-" * 30)
    hard_question = generator.generate_question("Quantitative Aptitude", "Hard")
    print(f"Question: {hard_question['question']}")
    print(f"Company: {hard_question['company_level']}")
    print(f"Topic: {hard_question['sub_topic']}")

def show_json_format():
    """Display complete JSON format"""
    
    generator = QuestionGenerator()
    
    print("\n\n📋 COMPLETE JSON FORMAT")
    print("=" * 60)
    
    question = generator.generate_question("Data Interpretation", "Medium")
    
    print("```json")
    print(json.dumps(question, indent=2, ensure_ascii=False))
    print("```")

def test_all_topics():
    """Generate questions from all available topics"""
    
    generator = QuestionGenerator()
    
    print("\n\n📚 ALL AVAILABLE TOPICS")
    print("=" * 60)
    
    for topic, subtopics in generator.topics.items():
        print(f"\n{topic}:")
        for subtopic in subtopics[:3]:  # Show first 3 subtopics
            try:
                question = generator.generate_question(topic, "Medium")
                print(f"  ✅ {subtopic}: Generated successfully")
            except Exception as e:
                print(f"  ❌ {subtopic}: {e}")

if __name__ == "__main__":
    demonstrate_company_levels()
    show_json_format()
    test_all_topics()