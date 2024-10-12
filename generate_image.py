import os
import base64
from together import Together
from PIL import Image
from io import BytesIO
from IPython.display import display

# Initialize Together.ai client
client = Together(api_key='6fe5089adec10f5f04b4f0d356d33d3f41d6d872edf612a8199c55bf65cc53c0')

def generate_image(prompt):
    # Call the Together.ai API to generate an image
    response = client.images.generate(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell-Free",
        width=1024,
        height=768,
        steps=1,
        n=1,
        response_format="b64_json"
    )

    # Extract the base64 image string from the response
    if response and response.data:
        b64_string = response.data[0].b64_json

        # Decode the base64 string
        image_data = base64.b64decode(b64_string)

        # Convert the binary data to a PIL image object
        image = Image.open(BytesIO(image_data))


        return image
    else:
        print(f"Failed to generate image for prompt: {prompt}")
        return None