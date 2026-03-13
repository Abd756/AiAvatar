from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Dict, Optional
from backend.app.schemas.session import BrainResponse
from backend.app.config import settings

class SessionController:
    def __init__(self):
        # Use Gemini if key is provided, otherwise fallback to OpenAI
        if settings.GEMINI_API_KEY:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.7,
            )
        else:
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=settings.OPENAI_API_KEY,
                temperature=0.7
            )
        self.output_parser = JsonOutputParser(pydantic_object=BrainResponse)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are a compassionate AI avatar guide for reflection sessions.\n"
             "YOUR RULES:\n"
             "1. NEVER give advice, opinions, or solutions.\n"
             "2. ALWAYS follow the provided script sequence.\n"
             "3. Keep responses short (1-2 sentences).\n"
             "4. If the user's answer is off-topic or too brief, use REASK.\n"
             "5. If the user is emotional, use ACKNOWLEDGE. Acknowledge warmth AND THEN ask the NEXT question: {next_question}\n"
             "6. If the answer is clear, use NEXT. Transition briefly AND THEN ask the NEXT question: {next_question}\n"
             "7. If there is NO next question (it's the end), use CLOSE.\n\n"
             "CONTEXT:\n"
             "Session Type: {script_context}\n"
             "Current Question being answered: {current_question}\n"
             "Next Question to ask: {next_question}\n\n"
             "Format your output as a JSON object with 'action', 'avatar_response', and 'thought_process' keys."
            ),
            ("user", "{user_input}")
        ])
        self.chain = self.prompt | self.llm | self.output_parser

    def process_turn(self, 
                     user_input: str, 
                     current_question: str, 
                     next_question: str,
                     script_context: str) -> Dict:
        try:
            # Synchornous wrapper for the chain if needed, or keeping it async
            # For now, let's keep it simple as a regular method if sessions.py calls it directly
            # Note: in sessions.py it was called without 'await', so it should be synchronous or a wrap
            return self.chain.invoke({
                "user_input": user_input,
                "current_question": current_question,
                "next_question": next_question if next_question else "NONE (This is the last question)",
                "script_context": script_context
            })
        except Exception as e:
            return {
                "action": "ERROR",
                "avatar_response": "I'm having a little trouble. Could you say that again?",
                "thought_process": str(e)
            }

session_controller = SessionController()
