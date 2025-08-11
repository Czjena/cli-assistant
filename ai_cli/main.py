import typer
from ai_cli.commands import generate, explain, review, interactive, generate_tests, checkproject
from ai_cli.commands.analyze_repo import analyze_repo as analyze_repo_func
from ai_cli.commands.createnewfile import create_new_file
from ai_cli.commands.context_adder import ContextAdder

app = typer.Typer(help="AI CLI - a tool for generating and analyzing code using a local LLM")

context_adder = ContextAdder(base_path='.')

@app.command()
def analyze(repo_path: str = typer.Argument(..., help="Path to github repository")):
    analyze_repo_func(repo_path)

@app.command()
def createnewfile(path: str = typer.Argument(..., help="Path to new file to create")):
    create_new_file(path)

@app.command()
def add_context_cmd(
    main_file: str = typer.Argument(..., help="Path to main source file"),
    prompt: str = typer.Argument(..., help="User prompt")
):
    full_prompt = context_adder.add_context(main_file, prompt)
    print(full_prompt)

    @app.command(name="interactive")
    def interactive_command(
            with_context: bool = typer.Option(False, help="Dołącz kontekst"),
            main_file: str = typer.Option(None, help="Ścieżka do pliku, którego kontekst dołączyć"),
    ):
        interactive.interactive_cli(with_context=with_context, main_file=main_file)

# Rejestracja innych komend:
app.command()(generate.generate)
app.command()(explain.explain)
app.command()(review.review)
app.command()(generate_tests.generate_tests)
app.command()(checkproject.analyze)

if __name__ == "__main__":
    app()
