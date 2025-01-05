import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def classify_message(content: str) -> str:
    """
    Classify a user message as 'food', 'weather', or 'unknown' using OpenAI.

    Args:
        content (str): User's message content.

    Returns:
        str: One of 'food', 'weather', or 'unknown'.
    """
    try:
        messages = [
            {"role": "system", "content": "You are an assistant that classifies user messages into categories. "
                                          "The categories are:\n"
                                          "1. 'food': If the message is related to food, recipes, or cooking.\n"
                                          "2. 'weather': If the message is related to weather or forecasts.\n"
                                          "3. 'unknown': If the message does not fit into the above categories."},
            {"role": "user", "content": f"Classify this message: {content}\n"
                                        "Respond with only one word: 'food', 'weather', or 'unknown'."}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=messages,
            max_tokens=5,
            temperature=0  # Reduce randomness
        )

        # Extract the classification
        classification = response.choices[0].message['content'].strip().lower()

        # Ensure valid classification
        if classification in ["food", "weather", "unknown"]:
            return classification
        return "unknown"
    
    except Exception:
        # Fallback for errors during classification
        return "unknown"
