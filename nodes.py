from llm import ask_gemini
from prompt import LLM_GUESS_PROMPT
from capture_browser import capture_wordle_board
from vision_feedback_agent import extract_full_state_from_image
from interact import type_guess
import time

MAX_ATTEMPTS = 6

def start(_: dict) -> dict:
    print("starting with SLATE...")
    time.sleep(2)
    type_guess("SLATE")


def get_state(_: dict) -> dict:
    img = capture_wordle_board()

    for attempt in range(1, 4):
        try:
            state = extract_full_state_from_image(img)
            print(f"🧠 Parsed state: {state}")
            return state
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if attempt < 3:
                print("🔁 Retrying state extraction...")
            else:
                raise ValueError("❌ Failed to extract state after 3 attempts.") from e

def ask_llm_guess(state: dict) -> dict:
    print("🤖 Asking LLM for next guess...")
    history = ""
    for i, (guess, result) in enumerate(zip(state.get("guesses", []), state.get("results", [])), start=1):
        history += f"- Guess {i}: {guess} → {result}\n"

    prompt = f"""{LLM_GUESS_PROMPT}

Previous Guesses and Feedback:
{history if history else 'None yet.'}

What is your next guess? Remember, you must follow the strategy guideline given to you to play intelligently.
""".strip()

    guess = ask_gemini(prompt).strip().upper()
    print(f"🔡 LLM guessed: {guess}")
    state["last_guess"] = guess
    return state

def submit_guess(state: dict) -> dict:
    guess = state.get("last_guess", "")
    print(f"⌨️ Typing guess into browser: {guess}")
    type_guess(guess)
    time.sleep(1) 
    return state

def check_result(state: dict) -> dict:
    print("🧾 Checking result from state...")
    last_guess = state.get("last_guess", "").upper()
    guesses = state.get("guesses", [])
    if "results" in state and last_guess in state["guesses"]:
        last_result = state["results"][state["guesses"].index(last_guess)]
        if all(r == "correct" for r in last_result):
            state["message"] = "🎉 You guessed it!"
            state["route"] = "End"
            return state

    if len(guesses) >= MAX_ATTEMPTS:
        state["message"] = "Game over! Max attempts reached."
        state["route"] = "End"
    else:
        state["route"] = "Get State"

    return state

def end(state: dict) -> dict:
    print(f"🏁 Game Ended. Final state:\n{state}")
    return state
