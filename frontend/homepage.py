import random
import json

import streamlit as st
from streamlit_lottie import st_lottie
from generators.model import generate_content
from generators.generate_image import generate_image  # Import the function from the earlier step
from concurrent.futures import ThreadPoolExecutor
from frontend.outputpage import show_output_page  # Import the function from outputpage.py

colors=['red','green','blue','black','while']

# Initialize session state for user_topic, story_output, generated_image, and page if they don't exist
if 'user_topic' not in st.session_state:
    st.session_state.user_topic = ""
if 'story_output' not in st.session_state:
    st.session_state.story_output = None
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []  # To store generated images
if 'page' not in st.session_state:
    st.session_state.page = "home"  # Add a session state for the current page

# Streamlit UI
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_loading_screen = load_lottie("frontend/assets/loading-screen-animation.json")

# Initialize session state to check if splash screen has been shown
if 'loading_shown' not in st.session_state:
    st.session_state['loading_shown'] = False

# Streamlit UI Home Page
if st.session_state.page == "home":
    st.title("📚 Story GPT")
    st.write("Enter a topic, and I'll generate a social story for you!")

    # User input
    st.session_state.user_topic = st.text_input("Enter a topic for the story:", st.session_state.user_topic)

    if st.button("Generate Story"):
        if st.session_state.user_topic:
            with st.spinner("Generating story and images ..."):
                # Splash screen logic
                if not st.session_state['loading_shown']:
                    st_lottie(
                        lottie_loading_screen,
                        speed=2,
                        reverse=False,
                        loop=True,
                        height=270,
                        width=None
                    )
                # Generate story content
                result = generate_content(st.session_state.user_topic)

                if result and result['story'] != '':
                    st.session_state.story_output = result  # Store output in session state
                    st.session_state.generated_images = []  # Clear previous images

                    # Prepare the full image prompts
                    context_description = f"the kid with brown hair, wearing a {random.choice(colors)} shirt and black pants.Image generated must be realistic"
                    image_prompts = [
                        f"{result['image_prompts'][i]}. Depict {context_description}."
                        for i in range(len(result['image_prompts']))
                    ]

                    # Function to generate images in parallel
                    def generate_image_concurrently(prompt):
                        return generate_image(prompt)

                    # Use ThreadPoolExecutor to generate images concurrently
                    with ThreadPoolExecutor() as executor:
                        generated_images = list(executor.map(generate_image_concurrently, image_prompts))

                    # Store the generated images in session state
                    for image in generated_images:
                        st.session_state.generated_images.append(image)

                    # Switch to the output page
                    st.session_state.page = "output"
                    st.rerun()  # Rerun to refresh the page and switch to output
                else:
                    st.warning('Topic may be explicit or invalid.')
        else:
            st.warning("Please enter a topic.")

# If page is set to 'output', call the show_output_page function
if st.session_state.page == "output":
    show_output_page()
