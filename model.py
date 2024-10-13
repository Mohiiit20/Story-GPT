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


def generate_story(topic):
    story_model = genai.GenerativeModel(model_name="tunedModels/socialstories-my8gxcmyb2vx", )

    story_session = story_model.start_chat(
        history=[]
    )

    story = story_session.send_message(f"Generate a social story on topic {topic}").text

    return {
        'story': story,
        'story_list': get_story_list(story)
    }


def generate_image_prompt(sentence):
    image_prompt_model = genai.GenerativeModel(model_name="tunedModels/imagepromptsgeneration-n56rok7p5r5v", )

    image_prompt_session = image_prompt_model.start_chat(
        history=[]
    )

    image_prompt = image_prompt_session.send_message(sentence).text

    return image_prompt


def generate_content(topic):
    story_data = generate_story(topic)
    story_sentences=story_data['story_list']
    image_prompts=[]
    for i in range(len(story_sentences)):
        image_prompts.append(generate_image_prompt(story_sentences[i]))

    for prompt in image_prompts:
        print(prompt)
        print('\n')

    return {
        'story': story_data['story'],
        'story_list': story_data['story_list'],
        'image_prompts': image_prompts
    }


def get_story_list(story):
    sentences = story.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    sentences = [s + '.' for s in sentences]
    print(sentences)
    return sentences