import os
import asyncio

from langchain_google_genai import ChatGoogleGenerativeAI
from backend.app.config import settings

async def validate_gemini():
    print("--- Gemini API Key Validation ---")
    
    key = os.getenv("GEMINI_API_KEY")
    if not key or "your_gemini_key_here" in key:
        print("❌ Error: GEMINI_API_KEY is not set correctly in your .env file.")
        return

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=key
        )
        response = await llm.ainvoke("Hello, are you active?")
        print("✅ Success! Gemini API key is valid.")
        print(f"Response: {response.content}")
    except Exception as e:
        print(f"❌ Gemini API Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(validate_gemini())
