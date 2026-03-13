import json
import os
from typing import List, Dict, Optional

class ScriptManager:
    def __init__(self, scripts_path: str = "backend/scripts"):
        self.scripts_path = scripts_path
        self.scripts = {}
        self.load_scripts()

    def load_scripts(self):
        if not os.path.exists(self.scripts_path):
            return
        
        for filename in os.listdir(self.scripts_path):
            if filename.endswith(".json"):
                path = os.path.join(self.scripts_path, filename)
                with open(path, "r") as f:
                    script_data = json.load(f)
                    name = script_data.get("script_name", filename)
                    self.scripts[name] = script_data

    def get_script(self, name: str) -> Optional[Dict]:
        return self.scripts.get(name)

    def get_question(self, script_name: str, index: int) -> Optional[Dict]:
        script = self.get_script(script_name)
        if script and "questions" in script:
            questions = script["questions"]
            if 0 <= index < len(questions):
                return questions[index]
        return None

script_manager = ScriptManager()
