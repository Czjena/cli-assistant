import os
import questionary

def choose_file(start_path="."):
    current_path = os.path.abspath(start_path)

    while True:
        # Lista folderów i plików w katalogu
        entries = os.listdir(current_path)
        entries = sorted(entries, key=lambda x: (not os.path.isdir(os.path.join(current_path, x)), x.lower()))

        # Dodaj możliwość "go up" jeśli nie jesteśmy w root
        choices = []
        if os.path.dirname(current_path) != current_path:
            choices.append(".. (go up)")

        choices.extend(entries)
        choices.append("Cancel")

        choice = questionary.select(f"Select a file or folder in: {current_path}", choices=choices).ask()

        if choice == "Cancel" or choice is None:
            return None  # użytkownik anulował

        if choice == ".. (go up)":
            current_path = os.path.dirname(current_path)
            continue

        selected_path = os.path.join(current_path, choice)

        if os.path.isdir(selected_path):
            # Wejdź do folderu
            current_path = selected_path
        else:
            # Wybrano plik, zwróć jego pełną ścieżkę
            return selected_path
