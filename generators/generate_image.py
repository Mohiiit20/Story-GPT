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
headers = {"Authorization": f"Bearer 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"}
print(hf_api_key)

def generate_image(prompt):
    def query(payload):
        try:
            print(f"Sending payload: {payload}")  # Print the payload being sent
            response = requests.post(API_URL, headers=headers, json=payload)
            print(f"Response status code: {response.status_code}")  # Print status code
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            return response.content
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
            print(f"Response text: {response.text}")  # Print response text for more details
            return None
        except Exception as err:
            print(f"Other error occurred: {err}")  # Log other errors
            return None

    image_bytes = query({"inputs": prompt})
    if image_bytes:
        return Image.open(io.BytesIO(image_bytes))  # Return PIL Image object
    else:
        print(f"Failed to generate image for prompt: {prompt}")
        return None
