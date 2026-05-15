import streamlit as st
import json

st.set_page_config(
    page_title="Generated Quiz",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Generated Quiz")

# CSS for better button styling (optional, but helps layout)
st.markdown("""
<style>
div.stButton > button:first-child {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

if "quiz_content" not in st.session_state:
    st.warning("No quiz generated yet. Please go back to the home page.")
    if st.button("Go to Home"):
        st.switch_page("app.py")
else:
    raw_content = st.session_state["quiz_content"]
    
    # Attempt to parse JSON
    try:
        # Sometimes LLMs wrap json in ```json ... ```, remove it if present
        clean_content = raw_content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content.replace("```json", "").replace("```", "")
        
        quiz_data = json.loads(clean_content)
        
        # Initialize user answers state if not exists
        if "user_answers" not in st.session_state:
            st.session_state["user_answers"] = {}

        for i, q in enumerate(quiz_data):
            st.markdown(f"#### Question {i+1}: {q['question']}")
            
            # Create 2x2 grid for options or just vertical 4
            # User asked for "four buttons", usually vertical is cleaner on mobile, but 2x2 is nice on desktop.
            # Let's do vertical for clarity as columns can get squished.
            
            options = q["options"]
            
            # Check if this question is already answered
            question_key = f"q_{i}"
            is_answered = question_key in st.session_state["user_answers"]
            
            if not is_answered:
                cols = st.columns(2) # 2x2 layout
                option_keys = list(options.keys())
                
                for idx, opt_key in enumerate(option_keys):
                    col = cols[idx % 2]
                    if col.button(f"{opt_key}: {options[opt_key]}", key=f"btn_{i}_{opt_key}"):
                        st.session_state["user_answers"][question_key] = opt_key
                        st.rerun()
            else:
                user_choice = st.session_state["user_answers"][question_key]
                correct_answer = q["answer"]
                
                # Show feedback
                if user_choice == correct_answer:
                    st.success(f"✅ Correct! The answer was {correct_answer}: {options[correct_answer]}")
                else:
                    st.error(f"❌ You selected {user_choice}. The correct answer was {correct_answer}: {options[correct_answer]}")

            st.markdown("---")

        # Score Calculation
        total_questions = len(quiz_data)
        answered_questions = len(st.session_state["user_answers"])
        
        if answered_questions == total_questions:
            score = 0
            for i, q in enumerate(quiz_data):
                question_key = f"q_{i}"
                user_choice = st.session_state["user_answers"].get(question_key)
                if user_choice == q["answer"]:
                    score += 1
            
            st.markdown("---")
            st.markdown(f"### 🏆 Quiz Completed!")
            st.markdown(f"#### Your Score: {score} / {total_questions}")
            
            percentage = (score / total_questions) * 100
            
            st.markdown("### 📊 Performance Analysis")
            
            if percentage == 100:
                st.balloons()
                st.success(f"🏆 **Perfect Score!** You're an absolute expert! 🌟✨")
                st.markdown("Highly impressive! You have a complete grasp of the material.")
            elif percentage >= 80:
                st.success(f"🥈 **Excellent Work!** Almost perfect! 🚀🔥")
                st.markdown("You have a very strong understanding. Just a few minor points to polish.")
            elif percentage >= 60:
                st.info(f"🥉 **Good Job!** You have a solid foundation. 👍📚")
                st.markdown("Well done! You've grasped most of the key concepts.")
            elif percentage >= 40:
                st.info(f"📈 **Fair Effort!** You're on the right track. 🧐📖")
                st.markdown("Good try! A bit more review will help you master these topics.")
            else:
                st.warning(f"🧊 **Keep Practicing!** Don't give up! 💪🎯")
                st.markdown("Every mistake is a learning opportunity. Review the content and try again!")

        if st.button("Create New Quiz"):
             del st.session_state["quiz_content"]
             if "user_answers" in st.session_state:
                 del st.session_state["user_answers"]
             st.switch_page("app.py")

    except json.JSONDecodeError:
        st.error("Error parsing quiz data. The raw output was not Valid JSON.")
        st.text_area("Raw Output", raw_content)
        if st.button("Go Back"):
            st.switch_page("app.py")
