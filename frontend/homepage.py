import streamlit as st
from model import generate_content

# Initialize session state for user_topic and story_output if they don't exist
if 'user_topic' not in st.session_state:
    st.session_state.user_topic = ""
if 'story_output' not in st.session_state:
    st.session_state.story_output = None

# Streamlit UI Home Page
st.title("📚 Story GPT")
st.write("Enter a topic, and I'll generate a social story, a split version, and an image prompt for you!")

# User input
st.session_state.user_topic = st.text_input("Enter a topic for the story:", st.session_state.user_topic)

if st.button("Generate Story"):
    if st.session_state.user_topic:
        with st.spinner("Generating story..."):
            result = generate_content(st.session_state.user_topic)
            if result and result['story'] != '':
                st.session_state.story_output = result  # Store output in session state
                st.success("Story generated!")
            else:
                st.warning('Topic may be explicit or invalid.')
    else:
        st.warning("Please enter a topic.")

# Displaying the generated story if it exists
if st.session_state.story_output:
    st.write(f"### Full Story\n{st.session_state.story_output['story']}")
    st.write(f"### Story in Parts\n1. {st.session_state.story_output['story_list'][0]}\n2. {st.session_state.story_output['story_list'][1]}")
    st.write(f"### Image Prompt\n{st.session_state.story_output['image_prompt']}")
