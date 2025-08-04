import typer

from ai_cli.commands import generate, explain, review, interactive # import funkcji

app = typer.Typer(help="AI CLI - a tool for generating and analyzing code using a local LLM")

app.command()(generate.generate)
app.command()(explain.explain)
app.command()(review.review)
app.command(name="interactive")(interactive.interactive_cli)
