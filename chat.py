import requests

API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "lfm2-1.2b"

def chat_with_model(prompt):
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
    }
    response = requests.post(API_URL, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]