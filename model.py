from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)


@st.cache_resource
def initialize_llm():
    return ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)


def generate_content(topic):
    story_model = genai.GenerativeModel(model_name="tunedModels/socialstories-my8gxcmyb2vx", )
    image_prompt_model = genai.GenerativeModel(model_name="tunedModels/imagepromptsgeneration-n56rok7p5r5v", )

    story_session = story_model.start_chat(
        history=[
        ]
    )

    image_prompt_session = image_prompt_model.start_chat(
        history=[
        ]
    )

    story = story_session.send_message(f"Generate a social story on topic {topic}").text

    image_prompt = image_prompt_session.send_message(story).text

    return {
        'story': story,
        'story_list': get_story_list(story),
        'image_prompt': image_prompt
    }


def get_story_list(story):
    sentences = story.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    sentences = [s + '.' for s in sentences]
    n = len(sentences) // 2
    return [" ".join(sentences[:n]), " ".join(sentences[n:])]
