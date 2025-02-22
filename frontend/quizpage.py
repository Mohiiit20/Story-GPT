import streamlit as st

def show_quiz_page(questions):
    st.title("Quiz Page")
    st.write("Answer the following questions:")

    # Define MCQs (placeholder questions)



    # Store user answers in session state
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}

    for i, q in enumerate(questions):
        st.subheader(f"Q{i+1}: {q['question']}")
        selected_option = st.radio(f"Select an answer for Q{i+1}", q["options"], key=f"q{i}")

        # Check answer when user selects an option
        if st.button(f"Submit Q{i+1}", key=f"submit_q{i}"):
            if selected_option == q["correct"]:
                st.success(f"✅ Correct! {selected_option} is the right answer.")
            else:
                st.error(f"❌ Incorrect! You chose {selected_option}.")
                st.success(f"✅ Correct Answer: {q['correct']}")

    # **Back button to return to the story output page**
    if st.button("Back to Story"):
        st.session_state.current_page = "output"
        st.rerun()
