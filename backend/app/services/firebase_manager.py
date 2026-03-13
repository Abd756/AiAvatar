import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from typing import Optional, List, Dict, Any
from backend.app.schemas.firebase import SessionState, TranscriptMessage
import os

class FirebaseManager:
    def __init__(self):
        self.db = None
        self._initialize()

    def _initialize(self):
        try:
            # Check for base64 encoded key first (for production)
            import base64
            import json
            
            encoded_key = os.getenv("FIREBASE_SERVICE_KEY_BASE64")
            if encoded_key:
                decoded_key = base64.b64decode(encoded_key).decode("utf-8")
                key_dict = json.loads(decoded_key)
                cred = credentials.Certificate(key_dict)
                print("✅ Firebase initialized using base64 environment variable.")
            else:
                # Fallback to local file
                key_path = "firebase_service_key.json"
                if not os.path.exists(key_path):
                    raise FileNotFoundError(f"Firebase key not found at {key_path}")
                
                cred = credentials.Certificate(key_path)
                print("✅ Firebase initialized using local JSON file.")
            
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        except Exception as e:
            print(f"❌ Firebase initialization error: {str(e)}")

    def create_session(self, session_id: str, script_name: str, user_name: Optional[str] = None) -> bool:
        try:
            session_ref = self.db.collection("sessions").document(session_id)
            state = SessionState(
                session_id=session_id,
                user_name=user_name,
                script_name=script_name
            )
            session_ref.set(state.dict())
            return True
        except Exception as e:
            print(f"❌ Error creating session: {str(e)}")
            return False

    def get_session_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        try:
            doc = self.db.collection("sessions").document(session_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"❌ Error getting session state: {str(e)}")
            return None

    def update_session_state(self, session_id: str, updates: Dict[str, Any]) -> bool:
        try:
            updates["updated_at"] = datetime.utcnow()
            self.db.collection("sessions").document(session_id).update(updates)
            return True
        except Exception as e:
            print(f"❌ Error updating session state: {str(e)}")
            return False

    def add_transcript_message(self, session_id: str, role: str, content: str) -> bool:
        try:
            message = TranscriptMessage(role=role, content=content)
            self.db.collection("sessions").document(session_id).collection("transcript").add(message.dict())
            return True
        except Exception as e:
            print(f"❌ Error adding transcript: {str(e)}")
            return False

    def list_scripts(self) -> List[Dict[str, Any]]:
        try:
            docs = self.db.collection("scripts").get()
            return [{"id": doc.id, "title": doc.to_dict().get("title", doc.id)} for doc in docs]
        except Exception as e:
            print(f"❌ Error listing scripts: {str(e)}")
            return []

    def get_script(self, script_id: str) -> Optional[Dict[str, Any]]:
        try:
            doc = self.db.collection("scripts").document(script_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"❌ Error getting script: {str(e)}")
            return None

# Global instance
firebase_manager = FirebaseManager()
