import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_get_script():
    print("--- Testing Get Script Detail Endpoint ---")
    
    # 1. List scripts to get an ID
    print("1. Listing scripts...")
    response = requests.get(f"{BASE_URL}/scripts")
    if response.status_code != 200:
        print(f"❌ Failed to list scripts: {response.text}")
        return
    
    scripts = response.json()
    if not scripts:
        print("❌ No scripts found in database.")
        return
    
    script_id = scripts[0]['id']
    print(f"✅ Found script: {script_id}")

    # 2. Get details for that script
    print(f"\n2. Fetching details for script: {script_id}...")
    response = requests.get(f"{BASE_URL}/scripts/{script_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Successfully fetched data.")
        print(f"   Title: {data.get('title')}")
        questions = data.get('questions', [])
        print(f"   Questions count: {len(questions)}")
        if questions:
            print(f"   First question: {questions[0]['text']}")
    else:
        print(f"❌ Failed to fetch script details: {response.text}")

if __name__ == "__main__":
    test_get_script()
