import streamlit as st
from PIL import Image

# Load a placeholder image (make sure to provide the correct path)
placeholder_image_path = "frontend/assets/loading-placeholder.png"  # Update this path
placeholder_image = Image.open(placeholder_image_path)

# Function to display the output page
def show_output_page():
    if st.session_state.story_output and st.session_state.generated_images:
        st.title(f"{st.session_state.user_topic}")

        # Display the story and generated images
        for i, story_part in enumerate(st.session_state.story_output['story_list']):
            st.write(f"{story_part}")

            # Check if the image is valid (not None)
            if st.session_state.generated_images[i] is not None:
                st.image(st.session_state.generated_images[i], caption=f"Generated Image {i + 1}", width=300)
            else:
                # Display placeholder image if the generated image is None
                st.image(placeholder_image, caption=f"Image {i + 1} could not be generated.", width=300)

        st.write("  \n  \n")

        # Create 3 buttons in a single row using Streamlit columns
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("PDF"):
                st.success("PDF button clicked")

        with col2:
            if st.button("Audio"):
                st.success("Audio button clicked")

        with col3:
            if st.button("Video"):
                st.success("Video button clicked")

        # Button to return to the home page
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()  # Rerun to switch back to the home page
    else:
        st.error("No content found. Please generate a story first.")
