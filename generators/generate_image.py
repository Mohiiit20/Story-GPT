import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
hf_api_key = os.getenv('HF_API_KEY')

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/merve/flux-lego-lora-dreambooth"
headers = {"Authorization": f"Bearer {hf_api_key}"}

# Image generation function
def generate_image(prompt, save_path=None):
    output_dir = os.path.dirname(save_path)

    def query(payload):
        try:
            print('----------------------------------------------------------------------\n')
            print(f"Sending payload: {payload}")  # Debugging info
            response = requests.post(API_URL, headers=headers, json=payload)
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()  # Raise error for bad responses
            return response.content
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response text: {response.text}")
            return None
        except Exception as err:
            print(f"Other error occurred: {err}")
            return None

    image_bytes = query({"inputs": prompt})
    if image_bytes:
        image = Image.open(io.BytesIO(image_bytes))
        if save_path:
            image.save(save_path)  # Save the image at the given path
            return save_path  # Return file path instead of Image object
        else:
            return image
    else:
        print(f"Failed to generate image for prompt: {prompt}")
        return None
