from chat import chat_with_model

def run_chat():
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
