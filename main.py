from features.chat_feature import run_chat
# from features.embedding_feature import run_embedding  # na przyszłość

def main():
    while True:
        print("\nWybierz funkcję:")
        print("1. Chat z modelem")
        print("2. Inna funkcja (w budowie)")
        print("0. Wyjście")
        choice = input("Wybierz: ")

        if choice == "1":
            run_chat()
        elif choice == "0":
            print("Do zobaczenia!")
            break
        else:
            print("Nieznana opcja, spróbuj ponownie.")

if __name__ == "__main__":
    main()
