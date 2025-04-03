#!/usr/bin/env python3
"""
Command-line interface for iedit.
"""

import os
import sys
import click
from pathlib import Path
from typing import List, Optional

from .latex_processor import LatexProcessor
from .bedrock_client import BedrockClient


@click.command()
@click.argument("file_or_directory", type=click.Path(exists=True))
@click.option(
    "--model",
    default="anthropic.claude-3-sonnet-20240229-v1:0",
    help="Bedrock model to use",
)
@click.option(
    "--recursive",
    is_flag=True,
    help="Process directories recursively",
)
@click.option(
    "--profile",
    help="AWS profile to use",
)
@click.option(
    "--region",
    default="us-west-2",
    help="AWS region to use",
)
def main(
    file_or_directory: str,
    model: str,
    recursive: bool,
    profile: Optional[str],
    region: str,
) -> None:
    """
    Edit LaTeX files to improve their form, syntax, and grammar using AI.
    
    FILE_OR_DIRECTORY can be a single LaTeX file or a directory containing LaTeX files.
    """
    try:
        # Initialize Bedrock client
        bedrock_client = BedrockClient(model=model, profile=profile, region=region)
        
        # Get list of files to process
        files_to_process = get_files_to_process(file_or_directory, recursive)
        
        if not files_to_process:
            click.echo(f"No LaTeX files found in {file_or_directory}")
            sys.exit(1)
            
        click.echo(f"Found {len(files_to_process)} LaTeX file(s) to process")
        
        # Process each file
        for file_path in files_to_process:
            click.echo(f"\nProcessing {file_path}")
            processor = LatexProcessor(file_path, bedrock_client)
            processor.process_file()
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


def get_files_to_process(file_or_directory: str, recursive: bool) -> List[Path]:
    """
    Get a list of LaTeX files to process.
    
    Args:
        file_or_directory: Path to a file or directory
        recursive: Whether to search directories recursively
        
    Returns:
        List of Path objects for LaTeX files to process
    """
    path = Path(file_or_directory)
    
    if path.is_file():
        if path.suffix.lower() == ".tex":
            return [path]
        else:
            click.echo(f"Warning: {path} is not a LaTeX file, skipping")
            return []
    
    # It's a directory, find all .tex files
    files = []
    
    if recursive:
        for tex_file in path.glob("**/*.tex"):
            files.append(tex_file)
    else:
        for tex_file in path.glob("*.tex"):
            files.append(tex_file)
            
    return files


if __name__ == "__main__":
    main()
