"""
Process LaTeX files and apply improvements.
"""

import os
import re
import difflib
import click
from pathlib import Path
from typing import List, Tuple
from colorama import Fore, Style, init

from .bedrock_client import BedrockClient

# Initialize colorama
init()


class LatexProcessor:
    """
    Process LaTeX files and apply improvements.
    """
    
    def __init__(self, file_path: Path, bedrock_client: BedrockClient):
        """
        Initialize the LaTeX processor.
        
        Args:
            file_path: Path to the LaTeX file
            bedrock_client: Bedrock client for AI processing
        """
        self.file_path = file_path
        self.bedrock_client = bedrock_client
        
    def process_file(self) -> None:
        """
        Process a LaTeX file and apply improvements.
        """
        # Read the file content
        with open(self.file_path, "r", encoding="utf-8") as f:
            original_content = f.read()
            
        # Split the content into chunks for processing
        chunks = self._split_into_chunks(original_content)
        
        # Process each chunk
        improved_chunks = []
        for i, chunk in enumerate(chunks):
            click.echo(f"\nProcessing chunk {i+1}/{len(chunks)}")
            
            # Get improved content from Bedrock
            improved_chunk = self.bedrock_client.improve_latex(chunk)
            
            # Show diff and ask for confirmation
            if self._show_diff_and_confirm(chunk, improved_chunk):
                improved_chunks.append(improved_chunk)
            else:
                improved_chunks.append(chunk)  # Keep original if not confirmed
                
        # Combine improved chunks
        improved_content = "\n\n".join(improved_chunks)
        
        # Write the improved content back to the file
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(improved_content)
            
        click.echo(f"\nSuccessfully processed {self.file_path}")
        
    def _split_into_chunks(self, content: str) -> List[str]:
        """
        Split LaTeX content into logical chunks for processing.
        
        Args:
            content: The full LaTeX content
            
        Returns:
            List of LaTeX chunks
        """
        # Simple approach: split by sections or subsections
        section_pattern = r"\\(section|subsection|subsubsection|chapter){"
        
        # Find all section markers
        section_matches = list(re.finditer(section_pattern, content))
        
        if not section_matches:
            # If no sections found, return the whole content as one chunk
            return [content]
            
        chunks = []
        
        # Add the preamble as the first chunk
        if section_matches[0].start() > 0:
            chunks.append(content[:section_matches[0].start()].strip())
            
        # Add each section as a chunk
        for i in range(len(section_matches)):
            start = section_matches[i].start()
            end = section_matches[i+1].start() if i < len(section_matches) - 1 else len(content)
            chunks.append(content[start:end].strip())
            
        return chunks
        
    def _show_diff_and_confirm(self, original: str, improved: str) -> bool:
        """
        Show the diff between original and improved content and ask for confirmation.
        
        Args:
            original: Original content
            improved: Improved content
            
        Returns:
            True if the user confirms the changes, False otherwise
        """
        # If no changes, return True
        if original == improved:
            click.echo("No changes needed for this chunk.")
            return True
            
        # Generate diff
        diff = list(difflib.unified_diff(
            original.splitlines(),
            improved.splitlines(),
            lineterm="",
            n=3  # Context lines
        ))
        
        # Print diff with colors
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                click.echo(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
            elif line.startswith("-") and not line.startswith("---"):
                click.echo(f"{Fore.RED}{line}{Style.RESET_ALL}")
            else:
                click.echo(line)
                
        # Ask for confirmation
        return click.confirm("Apply these changes?", default=True)
