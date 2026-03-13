import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SIMLI_API_KEY = os.getenv("SIMLI_API_KEY")
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME = "aiavatar_db"

settings = Config()
