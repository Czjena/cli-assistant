import questionary
from ai_cli.commands import generate, explain, review
import sys

from ai_cli.commands.listfiles import list_files_in_cwd


def interactive_cli():
    while True:
        choice = questionary.select(
            "Select an action:",
            choices=[
                "Generate code",
                "Explain code",
                "Review code",
                "List files in current folder",
                "Quit"
            ]
        ).ask()
        if choice == "List files in current folder":
            list_files_in_cwd()
            continue
        if choice == "Quit":
            print("Bye!")
            sys.exit(0)

        file = questionary.text("Enter file path:").ask()

        if choice == "Generate code":
            prompt = questionary.text("Enter prompt:").ask()
            generate.generate(file=file, prompt=prompt)
        elif choice == "Explain code":
            explain.explain(file=file)
        elif choice == "Review code":
            review.review(file=file)

