import requests

API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "lfm2-1.2b"

def chat_with_model(prompt):
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,
    }

    response = requests.post(API_URL, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]

def main():
    print("Chat CLI z LM Studio. Wpisz 'exit' aby zakończyć.")
    while True:
        prompt = input("Ty: ")
        if prompt.lower() in ["exit", "quit"]:
            print("Koniec rozmowy. Do zobaczenia!")
            break
        try:
            response = chat_with_model(prompt)
            print("Model:", response)
        except Exception as e:
            print("Błąd:", e)

if __name__ == "__main__":
    main()
