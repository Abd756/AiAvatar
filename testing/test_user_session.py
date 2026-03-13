import asyncio
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from backend.app.services.firebase_manager import firebase_manager

async def test_user_session():
    print("--- User Session Association Test ---")
    
    user_name = "Abdullah Test"
    # Format session ID like the frontend would
    session_id = f"abdullah_test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    script_name = "Daily Check-In"

    # 1. Create a session with user name
    print(f"\n1. Creating test session: {session_id} for user: {user_name}...")
    success = firebase_manager.create_session(session_id, script_name, user_name=user_name)
    if success:
        print("✅ Session created successfully.")
    else:
        print("❌ Failed to create session.")
        return

    # 2. Fetch back and verify user_name
    print(f"\n2. Verifying user_name for session: {session_id}...")
    state = firebase_manager.get_session_state(session_id)
    if state:
        retrieved_name = state.get('user_name')
        if retrieved_name == user_name:
            print(f"✅ User name correctly associated: {retrieved_name}")
        else:
            print(f"❌ User name mismatch: Expected '{user_name}', got '{retrieved_name}'")
    else:
        print("❌ Failed to retrieve session state.")

if __name__ == "__main__":
    asyncio.run(test_user_session())
