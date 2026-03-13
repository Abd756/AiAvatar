import asyncio
import os

from backend.app.services.session_controller import session_controller
from backend.app.services.script_manager import script_manager

async def run_test():
    print("--- AiAvatar Brain Logic Test ---")
    
    # Check if API Key is set
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        print("WARNING: Neither OPENAI_API_KEY nor GEMINI_API_KEY found in environment.")
        print("Please set your API key in the .env file.")
        return

    script_name = "Daily Check-In"
    question_idx = 0
    question_data = script_manager.get_question(script_name, question_idx)
    
    test_cases = [
        {"input": "I'm feeling a bit anxious but ready to talk.", "label": "Cooperative Answer"},
        {"input": "I don't know, just had some coffee.", "label": "Vague Answer"},
        {"input": "My dog is sleeping on the couch right now.", "label": "Off-topic Answer"}
    ]

    for case in test_cases:
        print(f"\n[Test Case]: {case['label']}")
        print(f"Avatar asked: {question_data['text']}")
        print(f"User said: {case['input']}")
        
        # Fetch next question for simulation
        next_question_data = script_manager.get_question(script_name, question_idx + 1)
        next_question = next_question_data["text"] if next_question_data else "Thank you for sharing. We are done."

        result = await session_controller.get_next_action(
            user_input=case['input'],
            current_question=question_data['text'],
            next_question=next_question,
            reask_count=0,
            max_reasks=2,
            script_name=script_name
        )
        
        print(f"Action: {result['action']}")
        print(f"Avatar Response: {result['avatar_response']}")
        print(f"Thought: {result['thought_process']}")

if __name__ == "__main__":
    asyncio.run(run_test())
