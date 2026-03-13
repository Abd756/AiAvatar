from fastapi import APIRouter, HTTPException
from backend.app.schemas.interaction import InteractionInput
from backend.app.services.firebase_manager import firebase_manager
from backend.app.services.session_controller import session_controller
from backend.app.services.script_manager import script_manager

router = APIRouter()

@router.get("/scripts")
async def list_scripts():
    return firebase_manager.list_scripts()

@router.get("/scripts/{script_id}")
async def get_script(script_id: str):
    script = firebase_manager.get_script(script_id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    return script

@router.post("/process-message")
async def process_message(data: InteractionInput):
    # 1. Fetch current session state from Firestore
    state_data = firebase_manager.get_session_state(data.session_id)
    
    # If session doesn't exist, initialize it
    if not state_data:
        # Default to "Daily Check-In" if no script_name provided or use provided name
        script_name = data.script_name if data.script_name else "Daily Check-In"
        firebase_manager.create_session(data.session_id, script_name, user_name=data.user_name)
        state_data = {
            "current_index": 0,
            "reask_count": 0,
            "script_name": script_name
        }

    current_index = state_data.get("current_index", 0)
    reask_count = state_data.get("reask_count", 0)
    persisted_script_name = state_data.get("script_name")
    
    # If the user requested a specific script and it's different from the one in the DB, reset progress
    script_selection = data.script_name if data.script_name else (persisted_script_name if persisted_script_name else "Daily Check-In")
    
    if persisted_script_name and data.script_name and persisted_script_name != data.script_name:
        # Script changed - Reset session
        current_index = 0
        reask_count = 0
        firebase_manager.update_session_state(data.session_id, {
            "current_index": 0,
            "reask_count": 0,
            "script_name": script_selection,
            "status": "in_progress"
        })

    # 2. Get the current question and the NEXT question from document
    script_id = script_selection.replace(" ", "_").lower()
    script_data_db = firebase_manager.get_script(script_id)
    
    if script_data_db:
        questions = script_data_db.get("questions", [])
        if current_index >= len(questions):
            return {
                "session_id": data.session_id,
                "message": "Session already completed", 
                "status": "completed",
                "brain_decision": {
                    "action": "CLOSE",
                    "avatar_response": "Thank you for sharing. We have completed our session for today.",
                    "thought_process": "Session index exceeds script length."
                }
            }
        
        question_data = questions[current_index]
        next_question_text = questions[current_index + 1]["text"] if current_index + 1 < len(questions) else None
    else:
        # Fallback to local script_manager for safety
        question_data = script_manager.get_question(script_selection, current_index)
        if not question_data:
            return {
                "session_id": data.session_id,
                "message": "Session already completed", 
                "status": "completed",
                "brain_decision": {
                    "action": "CLOSE",
                    "avatar_response": "Thank you for sharing. We have completed our session for today.",
                    "thought_process": "Fallback: Script manager returned no question."
                }
            }
        next_q_data = script_manager.get_question(script_selection, current_index + 1)
        next_question_text = next_q_data["text"] if next_q_data else None

    # 3. Decision Logic (The Brain)
    # Log user message to transcript
    firebase_manager.add_transcript_message(data.session_id, "user", data.user_input)

    # Process via LangChain - PASSING NEXT QUESTION TEXT TO PREVENT HALLUCINATION
    brain_decision = session_controller.process_turn(
        user_input=data.user_input,
        current_question=question_data["text"],
        next_question=next_question_text,
        script_context=f"Theme: {script_selection}"
    )

    # 4. State Management (Persistence)
    action = brain_decision["action"]
    is_completed = False
    
    if action == "NEXT" or action == "ACKNOWLEDGE":
        # For both NEXT and ACK, we advance the index
        new_index = current_index + 1
        is_completed = next_question_text is None
        firebase_manager.update_session_state(data.session_id, {
            "current_index": new_index,
            "reask_count": 0,
            "status": "in_progress" if not is_completed else "completed"
        })
    elif action == "REASK":
        new_reask_count = reask_count + 1
        if new_reask_count >= question_data.get("max_reasks", 3):
            # Force move to next after max reasks reached
            new_index = current_index + 1
            is_completed = next_question_text is None
            firebase_manager.update_session_state(data.session_id, {
                "current_index": new_index,
                "reask_count": 0,
                "status": "in_progress" if not is_completed else "completed"
            })
        else:
            firebase_manager.update_session_state(data.session_id, {
                "reask_count": new_reask_count
            })
    elif action == "CLOSE":
        is_completed = True
        firebase_manager.update_session_state(data.session_id, {
            "status": "completed"
        })

    # Log AI response to transcript
    firebase_manager.add_transcript_message(data.session_id, "avatar", brain_decision["avatar_response"])

    # Return structure matching what the user expects (and more)
    return {
        "session_id": data.session_id,
        "user_said": data.user_input,
        "avatar_asked": question_data["text"],
        "brain_decision": brain_decision,
        "is_completed": is_completed,
        "current_state": {
            "index": current_index,
            "reask_count": reask_count,
            "script": script_selection,
            "has_next": next_question_text is not None
        }
    }
