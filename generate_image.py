# import os
# import base64
# from together import Together
# from PIL import Image
# from io import BytesIO
# from IPython.display import display
#
# # Initialize Together.ai client
# client = Together(api_key='6fe5089adec10f5f04b4f0d356d33d3f41d6d872edf612a8199c55bf65cc53c0')
#
# def generate_image(prompt):
#     # Call the Together.ai API to generate an image
#     response = client.images.generate(
#         prompt=prompt,
#         model="black-forest-labs/FLUX.1-schnell-Free",
#         width=1024,
#         height=768,
#         steps=1,
#         n=1,
#         response_format="b64_json"
#     )
#
#     # Extract the base64 image string from the response
#     if response and response.data:
#         b64_string = response.data[0].b64_json
#
#         # Decode the base64 string
#         image_data = base64.b64decode(b64_string)
#
#         # Convert the binary data to a PIL image object
#         image = Image.open(BytesIO(image_data))
#
#
#         return image
#     else:
#         print(f"Failed to generate image for prompt: {prompt}")
#         return None

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
