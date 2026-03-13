import os
import sys
import json
import asyncio

# Add project root to path
sys.path.append(os.getcwd())

from backend.app.services.firebase_manager import firebase_manager

def load_json_scripts():
    scripts_dir = os.path.join("backend", "scripts")
    script_data = []
    
    for filename in os.listdir(scripts_dir):
        if filename.endswith(".json"):
            with open(os.path.join(scripts_dir, filename), "r") as f:
                data = json.load(f)
                script_data.append(data)
    return script_data

async def migrate():
    print("--- Migrating Scripts to Firestore ---")
    scripts = load_json_scripts()
    
    for script in scripts:
        title = script.get("title")
        print(f"Uploading: {title}...")
        
        # We'll use the title as the document ID for simplicity in this demo
        doc_id = title.replace(" ", "_").lower()
        
        try:
            firebase_manager.db.collection("scripts").document(doc_id).set(script)
            print(f"✅ Successfully uploaded {title}")
        except Exception as e:
            print(f"❌ Failed to upload {title}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(migrate())
