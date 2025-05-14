from llm import ask_gemini, ask_gemini_vision
from prompt import LLM_IMAGE_FEEDBACK_PROMPT
from PIL import Image
import ast

def extract_full_state_from_image(img: Image.Image) -> dict:
    response_text = ask_gemini_vision(LLM_IMAGE_FEEDBACK_PROMPT.strip(), img).strip()

    # Clean up triple-backtick + python wrapper
    if response_text.startswith("```"):
        parts = response_text.split("```")
        if len(parts) >= 2:
            response_text = parts[1].strip()
        if response_text.lower().startswith("python"):
            response_text = response_text[len("python"):].strip()

    if response_text.lower().startswith("json"):
        response_text = response_text[len("json"):].strip()

    try:
        feedback_data = ast.literal_eval(response_text)
    except Exception as e:
        raise ValueError(f"Failed to parse Gemini output: {e}\nRaw: {response_text}")

    return feedback_data
