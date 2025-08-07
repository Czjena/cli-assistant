import typer
from ai_cli.commands import generate, explain, review, interactive, generate_tests, checkproject
from ai_cli.commands.analyze_repo import analyze_repo as analyze_repo_func
from ai_cli.commands.createnewfile import create_new_file

app = typer.Typer(help="AI CLI - a tool for generating and analyzing code using a local LLM")

@app.command()
def analyze(repo_path: str = typer.Argument(..., help="Path to github repository")):
    analyze_repo_func(repo_path)

@app.command()
def createnewfile(path: str = typer.Argument(..., help="Path to new file to create")):
    create_new_file(path)


app.command()(generate.generate)
app.command()(explain.explain)
app.command()(review.review)
app.command(name="interactive")(interactive.interactive_cli)
app.command()(generate_tests.generate_tests)
app.command()(checkproject.analyze)

if __name__ == "__main__":
    app()