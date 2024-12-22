from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.message_crud import create_message, get_all_messages
from app.services.classification import classify_message
from app.services.vector_store import retrieve_relevant_documents
from app.services.weather_service import get_weather_data, generate_weather_response
from groq import Groq
import os

# Initialize the Groq client with the API key from environment variables
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

router = APIRouter()


@router.post("/messages/", summary="Classify and handle user messages", description="Classifies a user message as either 'food' or 'weather', generates an appropriate response using RAG or a weather API, and stores both the message and response in the database.")
def handle_message(content: str, db: Session = Depends(get_db)):
    """
    Handle user messages by:

    1. Classifying the message as "food" or "weather".
    2. Generating an appropriate response:
       - For "food": Use RAG with Groq for response generation.
       - For "weather": Fetch weather data and format a response.
    3. Storing the user message and AI response in the database.

    Args:
        content (str): The content of the user message.
        db (Session): Database session dependency.

    Returns:
        dict: Contains user message, AI response, and classification.
    """
    try:
        
        classification = classify_message(content) # Classify the message

        # Generate response based on classification
        if classification == "food":
            documents = retrieve_relevant_documents(content, collection_name="documents")
            if documents:
                response = generate_groq_response(content, documents)
            else:
                response = "I'm sorry, I couldn't find relevant information to answer your query."
        elif classification == "weather":
            weather_data = get_weather_data()
            response = generate_weather_response(weather_data)
        else:
            response = "I'm sorry, I can only handle food or weather queries."

        # Save user message and AI response in the database
        user_message = create_message(db=db, content=content, is_ai=False)
        ai_message = create_message(db=db, content=response, is_ai=True)

        # Return serialized response
        return {
            "user_message": {
                "id": user_message.id,
                "is_ai": user_message.is_ai,
                "content": user_message.content,
                "timestamp": user_message.timestamp
            },
            "ai_response": {
                "id": ai_message.id,
                "is_ai": ai_message.is_ai,
                "content": ai_message.content,
                "timestamp": ai_message.timestamp
            },
            "classification": classification
        }

    except Exception as e:
        print(f"Error handling message: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the message.")


@router.get("/messages/", summary="Retrieve all messages", description="Fetches all stored messages, including both user messages and AI responses, from the database.")
def get_all_messages_endpoint(db: Session = Depends(get_db)):
    """
    Retrieve all messages from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        list: List of all messages stored in the database.
    """
    try:
        return get_all_messages(db=db)
    except Exception as e:
        print(f"Error retrieving messages: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving messages.")


def generate_groq_response(query: str, documents: list) -> str:
    """
    Generate a response using Groq's Llama-3.3-70b-versatile model.

    Args:
        query (str): The user's query.
        documents (list): Retrieved documents for context.

    Returns:
        str: Generated response from the Groq model.
    """
    try:
        # Combining documents into a single context string
        context = "\n".join([doc["content"] for doc in documents if "content" in doc])

        # Constructing the prompt
        prompt = f"User Query: {query}\n\nContext:\n{context}\n\nAnswer:"

        # Using the Groq client to generate a response
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant for food-related queries."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=300
        )

        # Extract and return the response
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating response with Groq: {e}")
        return "Unable to generate a response at the moment."