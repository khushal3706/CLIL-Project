import requests
import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def test_chat(message, language):
    url = "http://127.0.0.1:5000/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {"message": message, "language": language}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            print(f"[{language.upper()}] Input: {message}")
            print(f"[{language.upper()}] Response: {result['response']}")
            print(f"[{language.upper()}] Original (EN): {result['original_en']}")
            print("-" * 30)
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    print("Testing Regional Language Chatbot API...")
    test_chat("नमस्ते", "hi")
    test_chat("வணக்கம்", "ta")
