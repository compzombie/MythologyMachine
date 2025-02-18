from fastapi import FastAPI, HTTPException
import openai
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Hardcoded question
HARD_CODED_QUERY = "Who are the Greek gods of war?"

# Function to call OpenAI API
def query_openai(prompt: str):
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an expert in mythology."},
                      {"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error querying OpenAI API: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# API route to get the AI response
@app.get("/ask")
def ask_openai():
    response = query_openai(HARD_CODED_QUERY)
    return {"question": HARD_CODED_QUERY, "response": response}
