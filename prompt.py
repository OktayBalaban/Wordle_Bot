LLM_GUESS_PROMPT = """
You are playing Wordle, a game where you must guess a hidden 5-letter English word. After each guess, you receive structured feedback for each letter:

- "correct"  → the letter is in the correct position (like a green tile)
- "present"  → the letter is in the word, but in a different position (like a yellow tile)
- "absent"   → the letter is not in the word at all (like a gray tile)

Your goal is to discover the hidden word in 6 guesses or fewer. You should reason strategically and avoid random guessing.

Here is your strategy guide:

1. **Start Strong with a High-Value Opener**
   Begin with a word that contains the most common letters in English. Good starters are:
   - SLATE, CRANE, AUDIO, RAISE, SOARE, ALERT

   These words test a variety of vowels and common consonants to maximize information gained.

2. **Understand the Feedback**
   After each guess, interpret the feedback list:
   - If a letter is marked "correct", always reuse it in the same position in future guesses.
   - If a letter is "present", include it again, but avoid placing it in the same position.
   - If a letter is "absent", avoid using it again — unless that letter appears multiple times and may be partially correct.

3. **Avoid Redundant Guesses**
   Do not repeat letters that are already confirmed "absent" — doing so wastes an opportunity to test new letters.

4. **Maximize Coverage Early**
   For the first 2–3 guesses, prioritize testing as many new, untried letters as possible — even if they are unlikely to be the answer.

   For example, after SLATE, follow up with a word like ROUND or CHIMP to test unused consonants.

5. **Handle Duplicates Carefully**
   Wordle allows repeated letters (e.g., SHEEP, BLOOD, LEVEL). If a letter is marked "present" or "correct" and you suspect it appears more than once, test that in future guesses.

6. **Track Eliminated Letters**
   Keep track of all letters marked "absent" and avoid reusing them unless you're testing for a known duplicate.

7. **Narrow the Solution Space**
   By the 3rd or 4th guess, you should have a partial structure of the word. Use logic to eliminate invalid combinations.

   Example:
   - Guess: SLATE → [absent, correct, present, absent, absent]
   - You now know that L is in position 2, and A is in the word but not at position 3. Try placing A elsewhere, keep L fixed, and eliminate S, T, and E.

8. **Respect Position Constraints**
   If a letter has been "present" multiple times but failed in specific positions, focus on the remaining untested positions.

9. **Avoid Obscure or Rare Words**
   Prioritize common English words likely to be used in Wordle. Avoid obscure, outdated, or ultra-rare words.

10. **Endgame Logic**
    If you have confirmed 3–4 letters by guess 5, use logic to permute the remaining structure. Focus on untested positions or substitutions with similar words.

---

### Feedback Interpretation Example:

Target Word: PLANK  
Guess: SLATE  
Feedback: ["absent", "correct", "present", "absent", "absent"]

Explanation:
- S is not in PLANK → "absent"  
- L is at the correct position (2nd) → "correct"  
- A is in the word, but not in position 3 → "present"  
- T and E are not in PLANK → "absent"

Use this logic on your previous guesses to eliminate wrong letters and improve your next one.

---

### Output Instructions:
- Respond with only your next guess as a single uppercase English word.
- Do not explain your reasoning.
- Do not reuse a previously guessed word.
- Do not use letters marked "absent" unless testing a duplicate.
- Do not include any punctuation or comments.

---

### Example-Based Reasoning Guide:

1. **Feedback:** ["absent", "correct", "absent", "absent", "absent"] (from SLATE)  
   → Next: **ROUND**  
   ✅ Tests unused letters, keeps L fixed  
   ❌ Avoid: **LEAST** (reuses known absents)

2. **Feedback:** ["absent", "present", "absent", "present", "absent"] (from CHAIR)  
   → Next: **THING**  
   ✅ Moves H/I to new positions, introduces new letters  
   ❌ Avoid: **HAIRS** (same positions, repeats absent letters)

3. **Feedback:** ["correct", "correct", "absent", "absent", "absent"] (from PLANT)  
   → Next: **PLUMB**  
   ✅ Keeps known correct P/L in place  
   ❌ Avoid: **PLANT** again

4. **Feedback:** ["present", "present", "absent", "absent", "absent"] (from BLOOD)  
   → Next: **BLANK**  
   ✅ Repositions B/L, avoids O/D  
   ❌ Avoid: **BLOOM** (repeats O which was absent)

---
"""


LLM_IMAGE_FEEDBACK_PROMPT = """
You are analyzing a screenshot of the Wordle game board.

Your job is to extract the **entire game state** so far by reading each guessed row and the tile colors.

A tile can be:
- "correct" → the letter is green (correct position)
- "present" → the letter is yellow (in the word, wrong position)
- "absent"  → the letter is gray (not in the word)

---

🔁 Output Format:
Respond with a Python dictionary **exactly** in the following structure:

{
  "guesses": [ "SLATE", "CLEAN", ... ],
  "results": [
    ["absent", "correct", "present", "absent", "present"],
    ["correct", "correct", "correct", "correct", "absent"]
  ],
  "keyboard": {
    "A": "correct",
    "B": "empty",
    "C": "correct",
    ...
    "Z": "empty"
  },
  "llm_round": 2,
  "last_guess": "CLEAN"
}

---

✅ Requirements:
- List all previous guesses from top to bottom of the board.
- Match each guess with its exact feedback result.
- Build a virtual keyboard status by combining all feedback:
  - If a letter is ever "correct", mark it "correct".
  - Else if "present", mark it "present".
  - Else if "absent", mark it "absent".
  - Otherwise, mark it "empty".
- Set "llm_round" to the number of guesses.
- Set "last_guess" to the most recent word guessed.

📌 Notes:
- Do not include the target word, even if visible.
- Do not include explanations.
- Only return a **valid Python dictionary** exactly in the format above.
"""