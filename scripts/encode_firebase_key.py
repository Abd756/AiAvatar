import base64
import os

def encode_key(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        print("\n--- FIREBASE_SERVICE_KEY_BASE64 ---")
        print(encoded)
        print("----------------------------------\n")
        print("Copy the string above and add it as an environment variable in Render.")

if __name__ == "__main__":
    encode_key("firebase_service_key.json")
