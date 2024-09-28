import streamlit as st
import pyrebase
import os
from dotenv import load_dotenv
from model import generate_content

# Load environment variables from .env file
load_dotenv()

# Firebase configuration
config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


# Function for user login
def login(email, password):
    try:
        # First, try to sign in the user
        user = auth.sign_in_with_email_and_password(email, password)

        # Now, check if the user exists in the Realtime Database
        user_data = firebase.database().child("users").child(email.replace('.', ',')).get()
        if user_data.val() is None:
            st.error("User does not exist in the database. Please sign up first.")
            return None

        # Validate the password against the database (if stored)
        stored_password = user_data.val().get("password")
        if stored_password == password:
            return user
        else:
            st.error("Incorrect password.")
            return None

    except Exception as e:
        st.error(f"Login failed: {e}")


# Function for user signup
def sign_up(email, password):
    try:
        # Check if the user already exists
        user_data = firebase.database().child("users").child(email.replace('.', ',')).get()
        if user_data.val() is not None:
            st.error("User already exists. Please log in.")
            return

        # Create the user in Firebase Auth
        auth.create_user_with_email_and_password(email, password)

        # Store the user data in the Realtime Database
        firebase.database().child("users").child(email.replace('.', ',')).set({
            "password": password  # Consider hashing the password for security
        })
        st.success("Sign-up successful! You can now log in.")
    except Exception as e:
        st.error(f"Sign-up failed: {e}")


# Streamlit UI
st.title("AI Story Generator")

if 'user' not in st.session_state:
    # Login form
    st.header("Login")
    email = st.text_input("Email", "")
    password = st.text_input("Password", "", type="password")

    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state['user'] = user
            st.success("Logged in successfully!")  # Show success message

    # Sign up form
    st.header("Or Sign Up")
    if st.button("Sign Up"):
        sign_up(email, password)

else:
    # Logged in user section
    st.success("Logged in successfully!")

    # Configure the page (This should be the first Streamlit command)
    # st.set_page_config(page_title="AI Story Generator", page_icon="📚")

    # Streamlit app content
    st.title("📚 AI Social Story Generator")
    st.write("Enter a topic, and I'll generate a social story, a split version, and an image prompt for you!")

    # User input
    user_topic = st.text_input("Enter a topic for the story:")

    if st.button("Generate Story"):
        if user_topic:
            with st.spinner("Generating content..."):
                result = generate_content(user_topic)
                if result and result['story'] != '':
                    st.success("Content generated!")
                    st.write(f"### Full Story\n{result['story']}")
                    st.write(f"### Story in Parts\n1. {result['story_list'][0]}\n2. {result['story_list'][1]}")
                    st.write(f"### Image Prompt\n{result['image_prompt']}")
                else:
                    st.warning('Topic may be explicit or invalid.')
        else:
            st.warning("Please enter a topic.")

    # Sidebar information
    st.sidebar.header("About")
    st.sidebar.write(
        "This app uses AI to generate short social stories for children with ASD. "
        "The stories are designed to teach social skills and manners related to the given topic, "
        "split into two parts, along with an image prompt for each story."
    )