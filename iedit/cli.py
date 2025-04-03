"""
Command-line interface for iedit.
"""
import click
from pathlib import Path
from typing import List, Optional

from .editor import LatexEditor
from .config import Config


@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--model', '-m', default='anthropic.claude-v2',
              help='Amazon Bedrock model to use')
@click.option('--config', '-c', type=click.Path(exists=True),
              help='Path to configuration file')
def main(files: List[str], model: str, config: Optional[str] = None) -> None:
    """
    Edit LaTeX files to improve their form, syntax and grammar using AI.
    
    FILES: One or more LaTeX files or directories containing LaTeX files.
    """
    try:
        # Load configuration
        cfg = Config(config_path=config) if config else Config()
        
        # Initialize editor
        editor = LatexEditor(model_id=model, config=cfg)
        
        # Process each input path
        for file_path in files:
            path = Path(file_path)
            if path.is_dir():
                # Process all .tex files in directory
                for tex_file in path.glob("**/*.tex"):
                    editor.process_file(tex_file)
            else:
                # Process single file
                editor.process_file(path)
                
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    main()