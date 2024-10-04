import streamlit as st
from model import generate_content
from PIL import Image
from generate_image import generate_image  # Import the function from the earlier step

# Initialize session state for user_topic, story_output, and generated_image if they don't exist
if 'user_topic' not in st.session_state:
    st.session_state.user_topic = ""
if 'story_output' not in st.session_state:
    st.session_state.story_output = None
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None

# Apply custom CSS for centering and styling
st.markdown("""
    <style>
        .centered-title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI Home Page
st.title("📚 Story GPT")
st.write("Enter a topic, and I'll generate a social story, a split version, and an image prompt for you!")

# User input
st.session_state.user_topic = st.text_input("Enter a topic for the story:", st.session_state.user_topic)

if st.button("Generate Story"):
    if st.session_state.user_topic:

        with st.spinner("Generating story and image ..."):
            # Generate story content
            result = generate_content(st.session_state.user_topic)
            if result and result['story'] != '':
                st.session_state.story_output = result  # Store output in session state
                st.success("Story generated!")

                # Display the title in bold and centered
                st.markdown(f"<div class='centered-title'>{st.session_state.user_topic}</div>", unsafe_allow_html=True)

                # Display the first part of the story
                st.write(f"{st.session_state.story_output['story_list'][0]}")

                # Placeholder for the image (before generating)
                image_placeholder = st.empty()
                image_placeholder.image("frontend/assets/loading-placeholder.png", caption="Generating Image...", width=350)

                # Display the second part of the story
                st.write(f"{st.session_state.story_output['story_list'][1]}")

                # Generate image based on the image prompt
                image_prompt = result['image_prompt']
                generated_img = generate_image(f"{image_prompt}")

                # Once image is ready, replace the placeholder and center the image
                if generated_img:
                    st.session_state.generated_image = generated_img  # Store the image in session state
                    image_placeholder.empty()  # Clear the loading placeholder

                    # Center the image by wrapping it in a <div> with inline CSS and increase the image size
                    st.markdown(f"""
                        <div style='text-align: center;'>
                            <img src='data:image/png;base64,{generated_img}' width='500'/>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning('Topic may be explicit or invalid.')
    else:
        st.warning("Please enter a topic.")
