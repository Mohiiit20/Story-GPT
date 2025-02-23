import streamlit as st
import fitz  # PyMuPDF
import io
import json
import random
from concurrent.futures import ThreadPoolExecutor
from streamlit_lottie import st_lottie
from generators.model import generate_content
from generators.generate_image import generate_image
from frontend.outputpage import show_output_page  # Import output page function
from generators.translator import INDIAN_LANGUAGES

colors = ['red', 'green', 'blue', 'yellow', 'orange', 'white']


def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF file."""
    text = ""
    with io.BytesIO(uploaded_file.read()) as pdf_stream:
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")
        for page in pdf_document:
            text += page.get_text("text") + "\n"
    return text

# Load Lottie animation
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_loading_screen = load_lottie("frontend/assets/loading-screen-animation.json")

# Initialize session state
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'user_topic' not in st.session_state:
    st.session_state.user_topic = ""
if 'story_output' not in st.session_state:
    st.session_state.story_output = None
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "en"
if 'loading_shown' not in st.session_state:
    st.session_state['loading_shown'] = False

st.title("Customized Story Generation")

# User input options
option = st.radio("Choose input method:", ("Enter text", "Upload PDF"))

if option == "Enter text":
    st.session_state.user_input = st.text_area("Enter your text:", st.session_state.user_input)
elif option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        st.session_state.user_input = extract_text_from_pdf(uploaded_file)

# Topic input
st.session_state.user_topic = st.text_input("Enter the topic of the story:", st.session_state.user_topic)

# Language selection dropdown
st.session_state.selected_language = st.selectbox(
    "Select a language for the story:",
    options=["en"] + list(INDIAN_LANGUAGES.keys()),
    format_func=lambda code: "English" if code == "en" else INDIAN_LANGUAGES[code].capitalize()
)

target_language = st.session_state.selected_language
if st.button("Generate Story"):
    if st.session_state.user_input and st.session_state.user_topic:
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
            result = generate_content(st.session_state.user_input)
            if result and result['story']:
                st.session_state.story_output = result
                st.session_state.generated_images = []

                # Generate image prompts
                context_description = "the kid with brown hair, wearing a colorful shirt and black pants. Image generated must be realistic." if target_language == 'en' else f"girl dressed in traditional attire, wearing a {random.choice(colors)} color. Image generated must be realistic."
                image_prompts = [
                    f"{result['image_prompts'][i]}. Depict {context_description}."
                    for i in range(len(result['image_prompts']))
                ]

                # Function to generate images in parallel
                def generate_image_concurrently(prompt, index):
                    save_path = f"generated_images/image_{index}.png"
                    return generate_image(prompt, save_path)

                # Use ThreadPoolExecutor to generate images concurrently
                with ThreadPoolExecutor() as executor:
                    generated_images = list(executor.map(generate_image_concurrently, image_prompts, range(len(image_prompts))))

                # Store generated images
                for image in generated_images:
                    st.session_state.generated_images.append(image)

                # Move to output page
                st.session_state.page = "output"
                st.rerun()
            else:
                st.warning("Invalid input or topic.")
    else:
        st.warning("Please provide input text and a topic.")

# If the page is set to 'output', call the output function
if st.session_state.page == "output":
    show_output_page()
