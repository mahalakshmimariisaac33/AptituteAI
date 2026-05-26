"""
🎯 AI Powered Streamlit Aptitude Trainer
Groq AI Version — Grey theme + Categories + Badges (NO TUTOR)
"""

import streamlit as st
from badges import BadgeSystem
import random

from ai_generator import generate_ai_question


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="🎯 AI Aptitude Trainer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================
# STYLES
# =========================

def inject_styles():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {display: none !important;}
    div[data-testid="collapsedControl"] {display: none !important;}

    .stApp { background: #f3f4f6; }

    .top-bar {
        background: linear-gradient(90deg, #facc15 0%, #eab308 100%);
        padding: 18px 28px;
        border-radius: 16px;
        color: #111827;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .top-bar h1 {
        font-size: 26px;
        font-weight: 900;
    }

    .stat-pill {
        background: rgba(0,0,0,0.08);
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 700;
        margin-left: 8px;
    }

    .card {
        background: white;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
    }

    .section-title {
        font-size: 13px;
        font-weight: 800;
        color: #6b7280;
        text-transform: uppercase;
    }

    div[data-testid="stButton"] > button {
        width: 100%;
        text-align: left;
        padding: 18px;
        border-radius: 12px;
        border: 2px solid #d1d5db;
        background: white;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    div[data-testid="stButton"] > button:hover {
        border-color: #facc15;
        background: #fef9c3;
    }

    </style>
    """, unsafe_allow_html=True)


# =========================
# SESSION INIT
# =========================

def initialize_session_state():

    if "initialized" not in st.session_state:

        st.session_state.initialized = True

        st.session_state.current_question = None
        st.session_state.question_answered = False
        st.session_state.selected_option = None
        st.session_state.last_answer_correct = None

        st.session_state.selected_category = "Quantitative Aptitude"
        st.session_state.selected_difficulty = "Medium"

        st.session_state.session_questions = 0
        st.session_state.session_correct = 0

        st.session_state.started = False

        # ✅ BADGE SYSTEM ONLY (TUTOR REMOVED)
        st.session_state.badge_system = BadgeSystem()


# =========================
# TOP BAR
# =========================

def display_top_bar():

    q = st.session_state.session_questions
    c = st.session_state.session_correct
    accuracy = (c / q * 100) if q else 0

    st.markdown(f"""
    <div class="top-bar">
        <div>
            <h1>🧠 AptitudeAI</h1>
            <p>AI Powered Placement Preparation</p>
        </div>
        <div>
            <span class="stat-pill">📝 Done: {q}</span>
            <span class="stat-pill">✅ Correct: {c}</span>
            <span class="stat-pill">🎯 Accuracy: {accuracy:.0f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# CATEGORY BAR
# =========================

def category_bar():

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        categories = [
            "Quantitative Aptitude",
            "Logical Reasoning",
            "Verbal Ability",
            "Data Interpretation"
        ]

        difficulties = ["Easy", "Medium", "Hard"]

        with col1:
            selected_category = st.selectbox(
                "📚 Category",
                categories,
                index=categories.index(st.session_state.selected_category)
            )

            if selected_category != st.session_state.selected_category:
                st.session_state.selected_category = selected_category
                st.session_state.current_question = None
                st.rerun()

        with col2:
            selected_difficulty = st.selectbox(
                "⚡ Difficulty",
                difficulties,
                index=difficulties.index(st.session_state.selected_difficulty)
            )

            if selected_difficulty != st.session_state.selected_difficulty:
                st.session_state.selected_difficulty = selected_difficulty
                st.session_state.current_question = None
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# QUESTION GENERATION
# =========================

def generate_question_safely():

    with st.spinner("🤖 Generating AI question..."):

        q = generate_ai_question(
            st.session_state.selected_category,
            st.session_state.selected_difficulty
        )

        return {
            "id": f"ai_{random.randint(1000,9999)}",
            "question": q["question"],
            "options": q["options"],
            "correct_answer": q["correct_answer"],
            "solution_steps": q["solution_steps"]
        }


# =========================
# QUESTION DISPLAY
# =========================

def display_question(q):

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {q['question']}")
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# ANSWER + BADGES ONLY
# =========================

def handle_answer_submission(q):

    badge_system = st.session_state.badge_system

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.session_state.question_answered:

        for opt in q["options"]:
            letter = opt[0]

            if letter == q["correct_answer"]:
                st.success(f"✔ {opt}")
            elif letter == st.session_state.selected_option:
                st.error(f"✘ {opt}")
            else:
                st.write(opt)

        st.markdown('</div>', unsafe_allow_html=True)
        return

    for opt in q["options"]:
        letter = opt[0]

        if st.button(opt, key=f"opt_{letter}"):

            is_correct = letter == q["correct_answer"]

            st.session_state.session_questions += 1
            if is_correct:
                st.session_state.session_correct += 1

            st.session_state.question_answered = True
            st.session_state.selected_option = letter
            st.session_state.last_answer_correct = is_correct

            # 🏅 BADGES ONLY
            badge_system.update_stats(is_correct, st.session_state.selected_category)
            new_badges = badge_system.check_badges()

            for b in new_badges:
                st.toast(f"🏅 Badge Unlocked: {b}")

            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# RESULTS (NO TUTOR)
# =========================

def display_results(q):

    if not st.session_state.question_answered:
        return

    if st.session_state.last_answer_correct:
        st.success("🎉 Correct Answer!")
        st.balloons()
    else:
        st.error(f"❌ Wrong Answer! Correct: {q['correct_answer']}")

    # ✅ SMALL EXPLANATION (NEW)
    st.markdown("### 💡 Explanation")

    explanation = q.get("solution_steps", "No explanation available.")

    # show only first 3–5 lines (small explanation)
    short_exp = "\n".join(explanation.split("\n")[:4])

    st.info(short_exp)

# =========================
# NEXT QUESTION
# =========================

def next_question():

    if st.session_state.question_answered:

        if st.button("➡️ Next Question", type="primary"):
            st.session_state.question_answered = False
            st.session_state.selected_option = None
            st.session_state.current_question = generate_question_safely()
            st.rerun()


# =========================
# MAIN
# =========================

def main():

    initialize_session_state()
    inject_styles()
    display_top_bar()
    category_bar()

    if not st.session_state.started:

        st.markdown("## 🚀 Start Practice")

        if st.button("Start"):
            st.session_state.started = True
            st.session_state.current_question = generate_question_safely()
            st.rerun()

        return

    if st.session_state.current_question is None:
        st.session_state.current_question = generate_question_safely()
        st.rerun()

    q = st.session_state.current_question

    display_question(q)
    handle_answer_submission(q)
    display_results(q)
    next_question()


if __name__ == "__main__":
    main()