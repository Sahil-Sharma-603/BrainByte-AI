import os
import json
from openai import OpenAI
from typing import Dict, Any
from dotenv import load_dotenv

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    system_prompt = """You are an expert coding challenge creator. 
    Your task is to generate a coding question with multiple choice answers.
    The question should be appropriate for the specified difficulty level.

    For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
    For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
    For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

    Return the challenge in the following JSON structure:
    {
        "title": "The question title",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct_answer_id": 0, // Index of the correct answer (0-3)
        "explanation": "Detailed explanation of why the correct answer is right"
    }

    Make sure the options are plausible but with only one clearly correct answer.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a {difficulty} coding challenge."}
            ],
            response_format= {"type": "json_object"},
            temperature=0.7,
            
        )

        # Parse the response content    
        response_content = response.choices[0].message.content
        challenge_data = json.loads(response_content)

        # Validate the response structure
        required_fields  = ["title", "options", "correct_answer_id", "explanation"]

        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing field: {field}")

        return challenge_data

    except Exception as e:
        print(f"Error generating challenge: {e}")
        # sample question
        return {
            "title": "What is the output of the following code?\n\n```python\nprint(2 + 3 * 4)\n```",
            "options": ["14", "20", "18", "11"],
            "correct_answer_id": 0,
            "explanation": "The correct answer is 14 because of operator precedence: multiplication is performed before addition."
        }
    

