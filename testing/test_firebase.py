import asyncio
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from backend.app.services.firebase_manager import firebase_manager

async def test_firebase():
    print("--- Firebase Firestore Connectivity Test ---")
    
    test_session_id = "test_session_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    script_name = "Daily Check-In"

    # 1. Create a session
    print(f"\n1. Creating test session: {test_session_id}...")
    success = firebase_manager.create_session(test_session_id, script_name)
    if success:
        print("✅ Session created successfully.")
    else:
        print("❌ Failed to create session.")
        return

    # 2. Add a transcript message
    print("\n2. Adding a test message to transcript...")
    success = firebase_manager.add_transcript_message(test_session_id, "user", "Hello Firebase!")
    if success:
        print("✅ Transcript message added.")
    else:
        print("❌ Failed to add message.")

    # 3. Update state
    print("\n3. Updating session state (moving to index 1)...")
    success = firebase_manager.update_session_state(test_session_id, {"current_index": 1, "reask_count": 0})
    if success:
        print("✅ Session state updated.")
    else:
        print("❌ Failed to update state.")

    # 4. Fetch back
    print("\n4. Fetching back the updated session...")
    state = firebase_manager.get_session_state(test_session_id)
    if state:
        print(f"✅ Data retrieved: Index={state.get('current_index')}, Script={state.get('script_name')}")
    else:
        print("❌ Failed to retrieve data.")

if __name__ == "__main__":
    asyncio.run(test_firebase())
