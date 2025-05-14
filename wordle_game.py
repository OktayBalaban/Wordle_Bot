MAX_ATTEMPTS = 6
WORD_LENGTH = 5
ALPHABET = list("QWERTYUIOPASDFGHJKLZXCVBNM")

def init_state():
    return {
        "guesses": [],
        "results": [],
        "keyboard": {ch: "empty" for ch in ALPHABET},
        "message": ""
    }

def check_guess(guess, target):
    guess = guess.upper()
    result = ["absent"] * WORD_LENGTH
    target_chars = list(target)
    for i in range(WORD_LENGTH):
        if guess[i] == target[i]:
            result[i] = "correct"
            target_chars[i] = None
    for i in range(WORD_LENGTH):
        if result[i] == "correct":
            continue
        if guess[i] in target_chars:
            result[i] = "present"
            target_chars[target_chars.index(guess[i])] = None
    return result

def update_keyboard(keyboard, guess, result):
    for ch, res in zip(guess, result):
        prev = keyboard.get(ch, "empty")
        if res == "correct" or (res == "present" and prev != "correct") or (res == "absent" and prev not in ["correct", "present"]):
            keyboard[ch] = res
    return keyboard

def wordle_guess(guess, state):
    state = state or init_state()
    guess = guess.strip().upper()
    target = state.get("target_word", "").upper()

    guesses = state["guesses"]
    results = state["results"]
    keyboard = state["keyboard"]

    if len(guess) != WORD_LENGTH:
        state["message"] = f"Please enter a {WORD_LENGTH}-letter word."
        return state, state["message"]

    if len(guesses) >= MAX_ATTEMPTS:
        return state, state.get("message", "")

    result = check_guess(guess, target)
    guesses.append(guess)
    results.append(result)
    keyboard = update_keyboard(keyboard, guess, result)

    state["guesses"] = guesses[:MAX_ATTEMPTS]
    state["results"] = results[:MAX_ATTEMPTS]
    state["keyboard"] = keyboard

    return state, state.get("message", "")