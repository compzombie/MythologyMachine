from fastapi import FastAPI, HTTPException
from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set. Please check your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize FastAPI
app = FastAPI()

# Hardcoded question
HARD_CODED_QUERY = "Who are the Greek gods of war?"

# Function to call OpenAI API using the new interface
def query_openai(prompt: str):
    try:
        logger.info(f"Querying OpenAI with prompt: {prompt}")
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are an expert in mythology."},
                {"role": "user", "content": prompt}
            ]
        )
        logger.info(f"Received response from OpenAI: {response}")
        return response.choices[0].message.content
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

# API route to get the AI response
@app.get("/ask")
def ask_openai():
    logger.info("Received request for /ask")
    response_data = query_openai(HARD_CODED_QUERY)
    logger.info("Returning response for /ask")
    return {"question": HARD_CODED_QUERY, "response": response_data}
