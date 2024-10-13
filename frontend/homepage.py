import streamlit as st
from model import generate_content
from PIL import Image
from generate_image import generate_image  # Import the function from the earlier step
from concurrent.futures import ThreadPoolExecutor

# Initialize session state for user_topic, story_output, and generated_image if they don't exist
if 'user_topic' not in st.session_state:
    st.session_state.user_topic = ""
if 'story_output' not in st.session_state:
    st.session_state.story_output = None
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []  # To store generated images

# Streamlit UI Home Page
st.title("📚 Story GPT")
st.write("Enter a topic, and I'll generate a social story, a split version, and an image prompt for you!")

# User input
st.session_state.user_topic = st.text_input("Enter a topic for the story:", st.session_state.user_topic)

if st.button("Generate Story"):
    if st.session_state.user_topic:
        with st.spinner("Generating story and images ..."):
            # Generate story content
            result = generate_content(st.session_state.user_topic)

            if result and result['story'] != '':
                st.session_state.story_output = result  # Store output in session state
                st.success("Story generated!")


                context_description = "a young boy with short brown hair, wearing a red shirt and blue jeans, with a curious expression"

                # Display the story lines
                st.write(f"### {st.session_state.user_topic.upper()}\n")
                st.session_state.generated_images = []  # Clear previous images

                # Prepare the full image prompts
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

                # Store the generated images in session state and display them
                for i, image in enumerate(generated_images):
                    st.session_state.generated_images.append(image)
                    st.write(f"{i + 1}. {result['story_list'][i]}")
                    st.image(image, caption=f"Generated Image {i + 1}", width=300)

            else:
                st.warning('Topic may be explicit or invalid.')
    else:
        st.warning("Please enter a topic.")
