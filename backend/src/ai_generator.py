
# import os
# import json
# import random
# import threading
# from collections import deque
# from typing import Dict, Any

# from google import genai
# from google.genai import types
# from dotenv import load_dotenv

# # ------------------------------------------------------------
# # Setup
# # ------------------------------------------------------------
# load_dotenv()
# client = genai.Client()  # Assumes GEMINI_API_KEY or GOOGLE_API_KEY is set in env

# # ------------------------------------------------------------
# # Categories: one full non-repeating pass, then random
# # ------------------------------------------------------------
# CATEGORIES = [
#     "Working Memory",
#     "Vocabulary",
#     "Grammar",
#     "Applied Math",
#     "Police Logic",
#     "Problem Solving",
#     "Map Navigation",
#     "Reading Comprehension",
# ]

# _lock = threading.Lock()
# _cycle = deque(random.sample(CATEGORIES, k=len(CATEGORIES)))  # shuffled once
# POST_CYCLE_RANDOM = True  # after first pass, pick randomly each call

# def get_next_category() -> str:
#     """Return the next category: pop from initial shuffled cycle; once empty, choose randomly."""
#     global _cycle
#     with _lock:
#         if _cycle:
#             return _cycle.popleft()
#         if POST_CYCLE_RANDOM:
#             return random.choice(CATEGORIES)
#         # If you prefer continuous non-repeating rounds, uncomment below:
#         # _cycle = deque(random.sample(CATEGORIES, k=len(CATEGORIES)))
#         # return _cycle.popleft()

# # ------------------------------------------------------------
# # Generator
# # ------------------------------------------------------------
# def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
#     category = get_next_category()

#     system_prompt = f"""
# You are an expert police-recruit exam item writer for the Winnipeg Police Service (WPS).
# Generate a single multiple-choice question aligned to the WPS Written Test, which assesses:
# - Working Memory
# - Vocabulary
# - Grammar
# - Applied Math
# - Police Logic
# - Problem Solving
# - Map Navigation
# - Reading Comprehension

# GIVEN CATEGORY (use this; do NOT choose your own): {category}

# GENERAL REQUIREMENTS
# - Output MUST be valid JSON matching the provided schema (title, options[4], correct_answer_id, explanation).
# - Exactly 4 options; only ONE is clearly correct. Distractors must be plausible and non-trivial.
# - Avoid any answer choices like “All of the above” or “None of the above.”
# - Use clear, plain language suitable for police recruits in Winnipeg (Canadian spelling is acceptable).
# - No programming or code content of any kind.
# - Keep any scenario content realistic but non-sensitive (no operational procedures, radio codes, or confidential tactics).

# DIFFICULTY
# - “easy”: single step or direct recall, short stimuli.
# - “medium”: 2–3 steps of reasoning or short scenario.
# - “hard”: multi-step reasoning, synthesis, or complex scenario with subtle distractors.

# CATEGORY-SPECIFIC RULES
# 1) Working Memory
#    - Provide a short list, description, or sequence (2–5 items). Ask the candidate to recall/apply it after a brief delay cue.
#    - Keep stimuli ≤ 40 words.

# 2) Vocabulary
#    - Ask for the best synonym/definition/usage of a word commonly found in policing contexts (e.g., “adherent,” “mitigate,” “precise”).
#    - If using a sentence, include 1 sentence only. No trick punctuation.

# 3) Grammar
#    - Focus on subject-verb agreement, pronoun case, punctuation, or sentence clarity.
#    - Provide ONE sentence and ask which revision is correct/clearest.

# 4) Applied Math
#    - Use everyday policing-relevant numeracy (rates, proportions, time, distance, perimeter/area, unit conversions).
#    - Round sensibly and state units. Provide only the necessary data.

# 5) Police Logic
#    - Present brief, neutral facts (2–5 lines). Ask which conclusion follows logically (no outside knowledge).
#    - Avoid legal advice or real procedures; this is pure reasoning.

# 6) Problem Solving
#    - Short scenario with conflicting constraints; ask for the best next step or prioritization.
#    - Options should reflect trade-offs and test judgment/ordering.

# 7) Map Navigation
#    - Use a small ASCII grid map (max 7×7) with legends (N/S/E/W streets or landmarks).
#    - Ask for shortest route, correct direction, or destination identification. Keep it readable in monospace.

# 8) Reading Comprehension
#    - Provide a passage of 90–180 words about a neutral topic (public notices, brief policies, community events).
#    - Ask about main idea, inference, specific detail, or author’s purpose.
#    - Passage must be self-contained; do NOT require external knowledge.

# EXPLANATIONS
# - Explain why the correct option is right AND why each distractor is wrong in 1–3 concise sentences total.
# - When the category is Vocabulary, Grammar, or Reading Comprehension, mention how communication clarity aids policing (e.g., accurate reports, court testimony, coordination).

# OUTPUT FORMAT (MUST MATCH THIS SCHEMA)
# {{
#   "title": "The question stem or prompt (include category in parentheses, e.g., 'Reading Comprehension')",
#   "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
#   "correct_answer_id": 0,
#   "explanation": "Why the correct answer is right and others are wrong (concise)."
# }}

# QUALITY CHECKS BEFORE YOU OUTPUT
# - Exactly 4 options; exactly one correct.
# - No ambiguity; the correct answer can be derived from the provided information.
# - Keep any ASCII map aligned and ≤ 7×7.
# - Keep any reading passage between 90–180 words.
# - Content is culturally neutral and suitable for a general audience.
# """

#     response_schema = {
#         'type': 'OBJECT',
#         'properties': {
#             'title': {'type': 'STRING'},
#             'options': {
#                 'type': 'ARRAY',
#                 'items': {'type': 'STRING'}
#             },
#             'correct_answer_id': {'type': 'INTEGER'},
#             'explanation': {'type': 'STRING'}
#         },
#         'required': ['title', 'options', 'correct_answer_id', 'explanation']
#     }
    
#     try:
#         response = client.models.generate_content(
#             model='gemini-2.5-flash',
#             contents=f"Generate a {difficulty} difficulty WPS written-test question for the category: {category}.",
#             config=types.GenerateContentConfig(
#                 system_instruction=system_prompt,
#                 response_mime_type='application/json',
#                 response_schema=response_schema,
#                 temperature=0.7
#             )
#         )
        
#         content = response.text
#         challenge_data = json.loads(content)

#         required_fields = ["title", "options", "correct_answer_id", "explanation"]
#         for field in required_fields:
#             if field not in challenge_data:
#                 raise ValueError(f"Missing required field: {field}")

#         # Sanity checks
#         if not isinstance(challenge_data["options"], list) or len(challenge_data["options"]) != 4:
#             raise ValueError("Options must be a list of exactly 4 strings.")
#         idx = challenge_data["correct_answer_id"]
#         if not isinstance(idx, int) or idx < 0 or idx > 3:
#             raise ValueError("correct_answer_id must be an integer 0–3.")

#         return challenge_data

#     except Exception as e:
#         # Keep your original-style fallback so the function always returns something
#         print("Generation error:", e)
#         return {
#             "title": f"[Fallback] {category} — Basic Check",
#             "options": [
#                 "Option A (correct)",
#                 "Option B",
#                 "Option C",
#                 "Option D",
#             ],
#             "correct_answer_id": 0,
#             "explanation": "Fallback item due to a generation error."
#         }


import os
import json
from typing import Dict, Any

from google import genai
from google.genai import types
from dotenv import load_dotenv

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------
load_dotenv()
client = genai.Client()  # Assumes GEMINI_API_KEY or GOOGLE_API_KEY in env

MODEL_NAME = os.getenv("WPS_MODEL_NAME", "gemini-2.5-flash")

CATEGORIES = [
    "Working Memory",
    "Vocabulary",
    "Grammar",
    "Applied Math",
    "Police Logic",
    "Problem Solving",
    "Map Navigation",
    "Reading Comprehension",
]

# ------------------------------------------------------------
# Core generator (now takes `category` from the caller)
# ------------------------------------------------------------
def generate_challenge_with_ai(difficulty: str, category: str) -> Dict[str, Any]:
    # Validate/normalize category from the UI
    if category not in CATEGORIES:
        category = "Vocabulary"  # fallback if a bad value is sent

    system_prompt = f"""
You are an expert police-recruit exam item writer for the Winnipeg Police Service (WPS).
Generate ONE multiple-choice question aligned to the WPS Written Test:
- Working Memory, Vocabulary, Grammar, Applied Math, Police Logic, Problem Solving, Map Navigation, Reading Comprehension.

GIVEN CATEGORY (use this; do NOT choose your own): {category}

STRICT OUTPUT (JSON ONLY; match schema): title, options[4], correct_answer_id, explanation.

!!!! CRITICAL RULES FOR `title` !!!!
- The `title` MUST contain the COMPLETE, self-contained question stem that includes ALL data needed to answer.
- The `title` MUST end with a question mark (?).
- If the category needs stimulus (passage/map/list), put it at the TOP of `title`, then a blank line, then the question.
- Do NOT use a short topic label as the title. The title is the FULL prompt the user reads to answer.

CATEGORY-SPECIFIC ADDITIONS
- Working Memory: include the 2–5 item list in the title, then ask the recall/apply question. Keep list ≤ 40 words.
- Vocabulary: include the target word or one short sentence with it; then ask for synonym/definition/usage.
- Grammar: include ONE sentence; ask which revision is correct/clearest.
- Applied Math: include all numbers/units in the title; then ask for the required result (with units).
- Police Logic: include 2–5 neutral facts (each on its own line) in the title; then ask which conclusion follows.
- Problem Solving: include a short scenario (3–5 lines) in the title; then ask for the best next step/prioritization.
- Map Navigation: include a ≤7×7 ASCII grid with a simple legend in the title; then ask the route/direction/destination.
- Reading Comprehension: include a 90–180 word passage in the title; then ask one question (main idea, inference, detail, purpose).

GENERAL REQUIREMENTS
- Exactly 4 options; only ONE correct; no “All/None of the above”.
- Clear, plain language (Canadian spelling OK). No code/programming content.
- Explanation: 1–3 concise sentences why the correct is right and others wrong.
- For Vocab/Grammar/Reading, note how communication clarity aids policing (e.g., reports, court testimony, coordination).

OUTPUT FORMAT
{{
  "title": "<FULL stem (incl. any passage/map/list). End with a question mark. Category tag in parentheses at the very end, e.g., '... ? (Applied Math)'>",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "correct_answer_id": 0,
  "explanation": "Short rationale."
}}

QUALITY CHECK BEFORE OUTPUT
- Title contains the full stem and ends with “?”.
- Any ASCII map aligned and ≤7×7; Reading passage 90–180 words.
- Exactly 4 options; exactly one correct; unambiguous from the provided stem.
"""


    response_schema = {
        'type': 'OBJECT',
        'properties': {
            'title': {'type': 'STRING'},
            'options': {
                'type': 'ARRAY',
                'items': {'type': 'STRING'}
            },
            'correct_answer_id': {'type': 'INTEGER'},
            'explanation': {'type': 'STRING'}
        },
        'required': ['title', 'options', 'correct_answer_id', 'explanation']
    }

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"Generate a {difficulty} difficulty WPS written-test question for the category: {category}.",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type='application/json',
                response_schema=response_schema,
                temperature=0.7
               
            )
        )

        content = response.text
        challenge_data = json.loads(content)

        # Validation
        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(challenge_data["options"], list) or len(challenge_data["options"]) != 4:
            raise ValueError("Options must be a list of exactly 4 strings.")
        idx = challenge_data["correct_answer_id"]
        if not isinstance(idx, int) or idx < 0 or idx > 3:
            raise ValueError("correct_answer_id must be an integer 0–3.")

        return challenge_data

    except Exception as e:
        print("Generation error:", e)
        return {
            "title": f"[Fallback] {category} — Basic Check",
            "options": [
                "Option A (correct)",
                "Option B",
                "Option C",
                "Option D",
            ],
            "correct_answer_id": 0,
            "explanation": "Fallback item due to a generation error."
        }
