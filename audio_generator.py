import requests
from io import BytesIO
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

xi_api_key = os.getenv('XI_API_KEY')


# Aria; 9BWtsMINqrJLrRacOk9x
# Roger; CwhRBWXzGAHq8TQ4Fs17
# Sarah; EXAVITQu4vr4xnSDxMaL
# Laura; FGY2WhTYpPnrIDTdsKH5
# Charlie; IKne3meq5aSn9XLyUdCD
# George; JBFqnCBsd6RMkjVDRZzb
# Callum; N2lVS1w4EtoT3dr4eOWO
# River; SAz9YHcvj6GT2YYXdXww
# Liam; TX3LPaxmHKxFdv7VOQHJ
# Charlotte; XB0fDUnXU5powFXDhCwa
# Alice; Xb7hH8MSUJpSbSDYk0k2
# Matilda; XrExE9yKIg1WjnnlVkGX
# Will; bIHbv24MWmeRgasZH58o
# Jessica; cgSgspJ2msm6clMCkdW9
# Eric; cjVigY5qzO86Huf0OWal
# Chris; iP95p4xoKVk53GoZ742B
# Brian; nPczCjzI2devNBz1zQrb
# Daniel; onwK4e9ZLuTAKqWW03F9
# Lily; pFZP5JQG7iQjIQuC4Bku
# Bill; pqHfZKP75CvOlQylNhV4


VOICE_ID = "EXAVITQu4vr4xnSDxMaL"


# Function to generate audio from text using ElevenLabs API
def generate_audio(text):
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    headers = {
        "Accept": "application/json",
        "xi-api-key": xi_api_key
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to generate audio
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    if response.ok:
        # Create an in-memory binary stream to hold the audio data
        audio_stream = BytesIO()
        for chunk in response.iter_content(chunk_size=1024):
            audio_stream.write(chunk)

        # Move the cursor to the beginning of the stream
        audio_stream.seek(0)
        return audio_stream
    else:
        print(f"Error: {response.text}")
        return None
