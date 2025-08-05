import logging
import questionary
from ai_cli.commands import generate, explain, review, generate_tests
import sys
from ai_cli.commands.choosefile import choose_file
from ai_cli.commands.createnewfile import create_new_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def interactive_cli(max_iterations=None):
    global file_path
    selected_file = None
    selected_languages = None

    logger.debug("Start interactive_cli")

    logger.debug("Asking for selected languages")
    selected_languages = questionary.checkbox(
        "Select languages/extensions to include in context (empty = all):",
        choices=[
            "python",
            "javascript",
            "typescript",
            "java",
            "go",
            "ruby"
        ],
    ).ask()
    logger.debug(f"Selected languages: {selected_languages}")

    if selected_languages is not None and len(selected_languages) == 0:
        selected_languages = "python"
        logger.debug("No languages selected, defaulting to 'python'")

    iteration = 0
    while True:
        iteration += 1
        logger.debug(f"Loop iteration {iteration}")
        if max_iterations and iteration > max_iterations:
            logger.debug("Maximum iterations reached, exiting")
            sys.exit(0)

        menu_choices = [
            "Create new file",
            "Choose file",
            "Generate code",
            "Explain code",
            "Review code",
            "Create unit tests",
            "Quit"
        ]

        logger.debug("Asking for menu choice")
        choice = questionary.select(
            "Select an action:",
            choices=menu_choices
        ).ask()
        logger.debug(f"Menu choice: {choice}")

        if choice == "Create new file":
            logger.debug("Create new file selected")
            file_path = questionary.text("Enter file path").ask()
            logger.debug(f"Entered file path: {file_path}")
            if file_path:
                create_new_file(file_path=file_path)
            else:
                logger.debug("No file path provided")
                continue

        if choice == "Quit":
            logger.info("Bye!")
            sys.exit(0)
            return

        if choice == "Choose file":
            logger.debug("Choose file selected")
            file_path = choose_file()
            if file_path:
                selected_file = file_path
                logger.debug(f"Selected file: {selected_file}")
            else:
                logger.debug("No file selected.")
            continue  # wracamy do menu

        if selected_file is None:
            logger.warning("No file selected yet. Please choose a file first.")
            continue  # wymuszamy wybór pliku przed dalszymi akcjami

        logger.debug(f"Processing choice '{choice}' with file '{selected_file}'")

        if choice == "Generate code":
            prompt = questionary.text("Enter prompt:").ask()
            logger.debug(f"Prompt entered: {prompt}")
            generate.generate(file=selected_file, prompt=prompt, languages=selected_languages)
        elif choice == "Explain code":
            explain.explain(file=selected_file)
        elif choice == "Review code":
            review.review(file=selected_file)
        elif choice == "Create unit tests":
            generate_tests.generate_tests(file_path=selected_file)
