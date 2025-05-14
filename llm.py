import google.generativeai as genai
import os
import requests
import base64
import requests
from PIL import Image
import io

def ask_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "❌ API key (GEMINI_API_KEY) not found in environment variables."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-05-06:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"⚠️ Unexpected format: {e}\n{response.json()}"
    else:
        return f"❌ Error {response.status_code}:\n{response.text}"
    

def ask_gemini_vision(prompt: str, image: Image.Image) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "❌ API key (GEMINI_API_KEY) not found."

    # Convert image to base64-encoded PNG
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-05-06:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": image_b64
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"⚠️ Unexpected format: {e}\n{response.json()}"
    else:
        return f"❌ Error {response.status_code}:\n{response.text}"