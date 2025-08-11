import logging
import questionary
from ai_cli.commands import generate, explain, review, generate_tests, context_adder
import sys
from ai_cli.commands.choosefile import choose_file
from ai_cli.commands.createnewfile import create_new_file
from ai_cli.commands.analyze_repo import analyze_repo
from ai_cli.commands.context_adder import ContextAdder


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
    context_adder = ContextAdder(base_path='.')  # inicjalizacja ContextAdder

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
            "Analyze repository",
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

        if choice == "Analyze repository with AI":
            repo_path = questionary.path("Enter path to repository:").ask()
            if not repo_path:
                logger.warning("No path provided.")
                continue
            output_path = questionary.text("Optional: path to save report (press enter to skip):").ask()
            if output_path == "":
                output_path = None
            analyze_repo(path=repo_path, output_path=output_path)

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

        # Tutaj pytamy, czy dołączyć kontekst
        with_context = questionary.confirm("Do you want to include related context from other files?").ask()

        # Teraz w zależności od wyboru dodajemy kontekst do promptu lub nie
        if choice == "Generate code":
            prompt = questionary.text("Enter prompt:").ask()
            logger.debug(f"Prompt entered: {prompt}")
            if with_context:
                prompt = context_adder.add_context(selected_file, prompt)
            generate.generate(file=selected_file, prompt=prompt, languages=selected_languages)

        elif choice == "Explain code":
            # Explain zwykle nie ma promptu, ale możemy dodać kontekst do pliku
            if with_context:
                # Możemy np. odczytać plik z kontekstem i przekazać jako argument (jeśli explain to wspiera)
                # Jeśli nie, to zostawiamy jak jest albo rozbudowujemy explain.
                # Dla przykładu:
                prompt = context_adder.add_context(selected_file, "")
                explain.explain(file=selected_file, extra_context=prompt)
            else:
                explain.explain(file=selected_file)

        elif choice == "Review code":
            if with_context:
                prompt = context_adder.add_context(selected_file, "")
                review.review(file=selected_file, extra_context=prompt)
            else:
                review.review(file=selected_file)

        elif choice == "Create unit tests":
            if with_context:
                prompt = context_adder.add_context(selected_file, "")
                generate_tests.generate_tests(file_path=selected_file, extra_context=prompt)
            else:
                generate_tests.generate_tests(file_path=selected_file)
