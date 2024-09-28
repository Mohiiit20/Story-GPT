import time
import streamlit as st
from frontend.authentication import login, sign_up
from frontend.landingpage import showLandingPage

# Streamlit UI

if 'user' not in st.session_state:
    # Login form
    st.set_page_config(page_title="StoryGPT Login", page_icon="📚")
    st.title("📚 Story GPT")
    st.header("Login")
    email = st.text_input("Email", "")
    password = st.text_input("Password", "", type="password")

    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state['user'] = user
            st.success("Logged in successfully!")
            time.sleep(2)
            st.rerun()

    # Sign up form
    st.header("Or Sign Up")
    if st.button("Sign Up"):
        sign_up(email, password)

else:
    # Logged-in user section
    showLandingPage()
