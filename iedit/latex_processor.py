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
            
        # Split the content into chunks with context for processing
        chunks_with_context = self._split_into_chunks(original_content)
        
        # Process each chunk
        improved_lines = original_content.splitlines()
        
        for i, (context_before, chunk, context_after) in enumerate(chunks_with_context):
            click.echo(f"\nProcessing chunk {i+1}/{len(chunks_with_context)}")
            
            # Display context and chunk
            if context_before:
                click.echo(f"\n{Fore.BLUE}--- Context (before) ---{Style.RESET_ALL}")
                click.echo(context_before)
            
            click.echo(f"\n{Fore.YELLOW}--- Chunk being edited (max 2 lines) ---{Style.RESET_ALL}")
            click.echo(chunk)
            
            if context_after:
                click.echo(f"\n{Fore.BLUE}--- Context (after) ---{Style.RESET_ALL}")
                click.echo(context_after)
            
            # Prepare full context for AI processing
            full_context = f"{context_before}\n\n{chunk}\n\n{context_after}" if context_before and context_after else chunk
            
            # Get improved content from Bedrock
            improved_chunk = self.bedrock_client.improve_latex(full_context)
            
            # Extract just the improved chunk part (corresponding to the original chunk)
            # This is a simplification - in a real implementation, you'd need more robust extraction
            improved_chunk_lines = improved_chunk.splitlines()
            context_before_lines = context_before.splitlines() if context_before else []
            context_after_lines = context_after.splitlines() if context_after else []
            
            # Extract the improved chunk (assuming the AI preserves structure)
            start_idx = len(context_before_lines) if context_before else 0
            end_idx = len(improved_chunk_lines) - len(context_after_lines) if context_after else len(improved_chunk_lines)
            extracted_improved_chunk = "\n".join(improved_chunk_lines[start_idx:end_idx])
            
            # Show diff and ask for confirmation
            if self._show_diff_and_confirm(chunk, extracted_improved_chunk):
                # Calculate the line indices in the original document
                chunk_start_line = sum(1 for _ in range(i * 2))  # Simplified - assumes fixed chunk size
                chunk_end_line = chunk_start_line + len(chunk.splitlines())
                
                # Replace the chunk in the improved lines
                improved_chunk_lines = extracted_improved_chunk.splitlines()
                improved_lines[chunk_start_line:chunk_end_line] = improved_chunk_lines
                
        # Combine improved lines
        improved_content = "\n".join(improved_lines)
        
        # Write the improved content back to the file
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(improved_content)
            
        click.echo(f"\nSuccessfully processed {self.file_path}")
        
    def _split_into_chunks(self, content: str) -> List[Tuple[str, str, str]]:
        """
        Split LaTeX content into small chunks of at most 2 lines for processing,
        with 5 lines of context before and after each chunk.
        
        Args:
            content: The full LaTeX content
            
        Returns:
            List of tuples containing (context_before, chunk, context_after)
        """
        # Split content into lines
        lines = content.splitlines()
        
        # Process in chunks of 2 lines
        chunk_size = 2
        context_size = 5
        
        chunks = []
        
        # Process the document in chunks of 2 lines
        for i in range(0, len(lines), chunk_size):
            # Get the current chunk (max 2 lines)
            end_idx = min(i + chunk_size, len(lines))
            current_chunk = "\n".join(lines[i:end_idx])
            
            # Get context before (5 lines)
            start_context_idx = max(0, i - context_size)
            context_before = "\n".join(lines[start_context_idx:i]) if i > 0 else ""
            
            # Get context after (5 lines)
            end_context_idx = min(len(lines), end_idx + context_size)
            context_after = "\n".join(lines[end_idx:end_context_idx]) if end_idx < len(lines) else ""
            
            # Add the chunk with its context
            chunks.append((context_before, current_chunk, context_after))
            
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
        click.echo("\n--- Proposed changes ---")
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                click.echo(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
            elif line.startswith("-") and not line.startswith("---"):
                click.echo(f"{Fore.RED}{line}{Style.RESET_ALL}")
            else:
                click.echo(line)
                
        # Ask for confirmation
        return click.confirm("Apply these changes?", default=True)
