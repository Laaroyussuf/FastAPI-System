# **Conversational AI Platform**

## **Overview**
This project implements a backend system using **FastAPI** and **SQLAlchemy ORM** for a conversational AI platform. The platform handles:
- **Message classification** (food or weather).
- **AI response generation** using:
  - **RAG (Retrieval-Augmented Generation)** for food queries with **Llama-3.3-70b-versatile (Groq)**.
  - **Weather API** with **GPT-4** for weather queries.
- **Document processing and vector storage** using **ChromaDB**.

---

## **Features**
- **Message Classification**: Determines whether a user query relates to food or weather.
- **RAG for Food Queries**: Uses Llama-3.3-70b with Groq for food-related questions.
- **Weather Query Response**: Retrieves weather data from a weather API for New York and generates responses in natural language using GPT-4.
- **PDF Document Processing**:
  - Splits uploaded PDFs into pages.
  - Embeds the text content into **ChromaDB** using `text-embedding-3-small`.

---

## **Setup Instructions**
### **Prerequisites**
- Python 3.9 or higher
- API keys:
  - **OpenAI** for GPT-4 and embeddings.
  - **Groq** for RAG-based food query response.
  - **WeatherAPI** for weather data.
- SQLite

### **Installation**
1. Clone the repository:
```bash
git clone https://github.com/Laaroyussuf/FastAPI-System.git
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a .env file in the project root:
```env
OPENAI_API_KEY=<your-openai-api-key>
GROQ_API_KEY=<your-groq-api-key>
WEATHER_API_KEY=<your-weather-api-key>
```
Replace placeholders with your API keys.

5. Initialize the database:
```bash
python app/database.py
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

### **API Endpoints**
**1. POST /messages**
Description: Classifies user messages as food or weather and generates AI responses.
Request:
```json
{
"content": "How do I prepare pasta?"
}
```
Response:
```json
{
"user_message": {
"id": 1,
"is_ai": false,
"content": "How do I prepare pasta?",
"timestamp": "2024-12-22T10:00:00"
  },
"ai_response": {
"id": 2,
"is_ai": true,
"content": "Here is how you can prepare pasta...",
"timestamp": "2024-12-22T10:00:01"
  },
"classification": "food"
}
```

**2. POST /documents**
Description: Uploads a PDF, splits it into pages, and stores embeddings in ChromaDB.
Request: Upload a .pdf file.
Response:
```json
{
"message": "Document uploaded and processed successfully.",
"document_id": 1
}
```

**3. GET /messages**
Description: Retrieves all stored messages from the database.
Response:
```json
[
{
"id": 1,
"is_ai": false,
"content": "How do I prepare pasta?",
"timestamp": "2024-12-22T10:00:00"
},
{
"id": 2,
"is_ai": true,
"content": "Here is how you can prepare pasta...",
"timestamp": "2024-12-22T10:00:01"
}
]
```

### **Assumptions**
1. User queries are text-based and can relate to food or weather.
2. All PDFs are valid and can be processed into text.
3. ChromaDB is the chosen vector database for storage.

### **Testing Instructions**
Run the FastAPI server:
```bash
uvicorn app.main:app --reload
```

### **Access the Swagger documentation at:**
```arduino
http://127.0.0.1:8000/docs
```
Use the available endpoints to test functionality.

### **Folder Structure**
```bash
    /app
    ├── crud
    ├── models.py
    ├── database.py
    ├── routers
    ├── services
    ├── main.py
