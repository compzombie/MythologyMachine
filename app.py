from fastapi import FastAPI
import openai
import os

# Load OpenAI API Key (Make sure to set this in your environment variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Hardcoded question
HARD_CODED_QUERY = "Who are the Greek gods of war?"

# Function to call OpenAI API
def query_openai(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert in mythology."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# API route to get the AI response
@app.get("/ask")
def ask_openai():
    response = query_openai(HARD_CODED_QUERY)
    return {"question": HARD_CODED_QUERY, "response": response}
