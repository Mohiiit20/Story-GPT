import streamlit as st
import time
from streamlit_lottie import st_lottie
import json

# Load Lottie animation for correct answers
def load_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_correct_answer = load_lottie("frontend/assets/celebration-animation.json")  # Replace with your own animation

def show_quiz_page(questions):
    st.title("Quiz Page")
    st.write("Answer the following questions:")

    # Store user answers in session state
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}

    for i, q in enumerate(questions):
        st.subheader(f"Q{i+1}: {q['question']}")

        # Ensure no default selection
        selected_option = st.radio(
            f"Select an answer for Q{i+1}",
            q["options"],
            index=None,  # No default selection
            key=f"q{i}"
        )

        # Check answer when user submits
        if st.button(f"Submit Q{i+1}", key=f"submit_q{i}"):
            if selected_option:
                if selected_option == q["correct"]:
                    st.success(f"✅ Correct! {selected_option} is the right answer.")

                    # Display Lottie animation for 2 seconds
                    lottie_placeholder = st.empty()
                    with lottie_placeholder:
                        st_lottie(
                            lottie_correct_answer,
                            speed=1,
                            reverse=False,
                            loop=False,
                            height=250,
                            width=None
                        )
                    time.sleep(2)  # Pause for 2 seconds
                    lottie_placeholder.empty()  # Remove animation after 2 seconds

                else:
                    st.error(f"❌ Incorrect! You chose {selected_option}.")
                    st.success(f"✅ Correct Answer: {q['correct']}")
            else:
                st.warning("⚠️ Please select an answer before submitting.")

    # **Back button to return to the story output page**
    if st.button("Back to Story"):
        st.session_state.current_page = "output"
        st.rerun()
