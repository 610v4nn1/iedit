"""
Command-line interface for iedit.
"""

import os
import sys
import click
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm

from iedit.editor import LatexEditor
from iedit.bedrock import get_available_models

console = Console()

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--model', '-m', help='Amazon Bedrock model to use for editing', 
              default='anthropic.claude-v2')
@click.option('--recursive', '-r', is_flag=True, help='Process directories recursively')
@click.option('--yes', '-y', is_flag=True, help='Apply all suggested changes without confirmation')
@click.option('--config', '-c', help='Path to configuration file', 
              type=click.Path(exists=True), default=None)
@click.option('--list-models', is_flag=True, help='List available Amazon Bedrock models')
@click.version_option()
def main(path, model, recursive, yes, config, list_models):
    """
    iedit - A CLI tool for editing LaTeX files to improve form, syntax, and grammar using AI.
    
    PATH can be a single LaTeX file or a directory containing LaTeX files.
    """
    if list_models:
        models = get_available_models()
        console.print("Available Amazon Bedrock models:")
        for m in models:
            console.print(f"  - {m}")
        return

    path = Path(path)
    
    try:
        editor = LatexEditor(model=model, config_path=config, auto_apply=yes)
        
        if path.is_file():
            if path.suffix.lower() != '.tex':
                console.print(f"[yellow]Warning: {path} does not appear to be a LaTeX file.[/yellow]")
                if not Confirm.ask("Continue anyway?"):
                    return
            process_file(editor, path)
        elif path.is_dir():
            process_directory(editor, path, recursive)
        else:
            console.print(f"[red]Error: {path} is neither a file nor a directory.[/red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

def process_file(editor, file_path):
    """Process a single LaTeX file."""
    console.print(f"Processing [bold]{file_path}[/bold]...")
    editor.edit_file(file_path)
    console.print(f"[green]Finished processing {file_path}[/green]")

def process_directory(editor, dir_path, recursive=False):
    """Process all LaTeX files in a directory."""
    console.print(f"Processing LaTeX files in [bold]{dir_path}[/bold]...")
    
    for item in dir_path.iterdir():
        if item.is_file() and item.suffix.lower() == '.tex':
            process_file(editor, item)
        elif recursive and item.is_dir():
            process_directory(editor, item, recursive)
    
    console.print(f"[green]Finished processing directory {dir_path}[/green]")

if __name__ == '__main__':
    main()