import typer
from pathlib import Path
import difflib
from rich.console import Console
from rich.text import Text

from iedit.bedrock import BedrockClient
from iedit.editor import LatexEditor

app = typer.Typer()
console = Console()

def _edit_file(file_path: Path):
    """
    Performs the editing process for a single file.
    """
    typer.echo(f"Editing file: {file_path}")

    bedrock_client = BedrockClient()
    editor = LatexEditor(file_path, bedrock_client)

    new_chunks = []
    try:
        for original, polished in editor.edit():
            if polished is None:
                new_chunks.append(original)
                continue

            if original.strip() == polished.strip():
                new_chunks.append(original)
                continue

            console.print("Original:", style="bold red")
            console.print(original)
            console.print("Polished:", style="bold green")
            console.print(polished)

            diff = difflib.unified_diff(
                original.splitlines(keepends=True),
                polished.splitlines(keepends=True),
                fromfile='original',
                tofile='polished',
            )

            text = Text()
            for line in diff:
                if line.startswith('+'):
                    text.append(line, style="green")
                elif line.startswith('-'):
                    text.append(line, style="red")
                elif line.startswith('^'):
                    text.append(line, style="blue")
                else:
                    text.append(line)
            console.print(text)

            if typer.confirm("Apply this change?"):
                new_chunks.append(polished)
            else:
                new_chunks.append(original)
    except Exception as e:
        typer.echo(f"An error occurred while processing {file_path}: {e}")
        # In case of an error with one file, we can decide to continue with the next
        # For now, let's just print the error and move on.
        return

    new_content = "\n\n".join(new_chunks)
    file_path.write_text(new_content)
    typer.echo(f"File {file_path} saved.")


@app.command()
def edit(path: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=True, readable=True, help="Path to the LaTeX file or directory to edit.")):
    """
    Edit a LaTeX file or all .tex files in a directory to improve their form, syntax, and grammar.
    """
    if path.is_file():
        if path.suffix == ".tex":
            _edit_file(path)
        else:
            typer.echo(f"Error: The specified file is not a .tex file.")
            raise typer.Exit(code=1)
    elif path.is_dir():
        tex_files = list(path.glob("**/*.tex"))
        if not tex_files:
            typer.echo("No .tex files found in the specified directory.")
            return

        for tex_file in tex_files:
            _edit_file(tex_file)

@app.command()
def test_bedrock(prompt: str):
    """
    Test the Bedrock integration with a given prompt.
    """
    client = BedrockClient()
    response = client.invoke_model(prompt)
    typer.echo(response)

if __name__ == "__main__":
    app()
