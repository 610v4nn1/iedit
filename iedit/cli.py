"""
Command-line interface for iedit
"""
import os
import click
from .editor import LatexEditor
from .config import load_config

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--model', '-m', help='Bedrock model to use', default='anthropic.claude-v2')
@click.option('--config', '-c', type=click.Path(), help='Path to config file')
@click.option('--recursive', '-r', is_flag=True, help='Process directories recursively')
def main(path, model, config, recursive):
    """
    Edit LaTeX files to improve their form, syntax and grammar using AI.
    
    PATH can be either a .tex file or a directory containing .tex files.
    """
    try:
        config_data = load_config(config) if config else {}
        editor = LatexEditor(model=model, **config_data)
        
        if os.path.isfile(path):
            if not path.endswith('.tex'):
                click.echo(f"Error: {path} is not a LaTeX file", err=True)
                return 1
            editor.process_file(path)
        else:  # directory
            if recursive:
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.endswith('.tex'):
                            editor.process_file(os.path.join(root, file))
            else:
                for file in os.listdir(path):
                    if file.endswith('.tex'):
                        editor.process_file(os.path.join(path, file))
                        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        return 1
    
    return 0

if __name__ == '__main__':
    main()