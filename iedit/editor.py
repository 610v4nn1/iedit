"""
Core functionality for editing LaTeX files.
"""
import re
from pathlib import Path
from typing import List, Tuple, Optional
import boto3
import click

from .config import Config


class LatexEditor:
    def __init__(self, model_id: str, config: Config):
        """
        Initialize the LaTeX editor.
        
        Args:
            model_id: ID of the Amazon Bedrock model to use
            config: Configuration object
        """
        self.model_id = model_id
        self.config = config
        self.bedrock = boto3.client('bedrock-runtime')
        
    def process_file(self, file_path: Path) -> None:
        """
        Process a single LaTeX file.
        
        Args:
            file_path: Path to the LaTeX file
        """
        if not file_path.suffix == '.tex':
            click.echo(f"Skipping non-LaTeX file: {file_path}")
            return
            
        click.echo(f"Processing {file_path}...")
        
        # Read the file content
        content = file_path.read_text()
        
        # Split into chunks while preserving LaTeX structure
        chunks = self._split_content(content)
        
        # Process each chunk
        modified_chunks = []
        for chunk in chunks:
            suggestions = self._get_suggestions(chunk)
            if suggestions:
                modified_chunk = self._apply_suggestions(chunk, suggestions)
                modified_chunks.append(modified_chunk)
            else:
                modified_chunks.append(chunk)
                
        # Combine chunks and write back
        modified_content = ''.join(modified_chunks)
        if modified_content != content:
            backup_path = file_path.with_suffix(file_path.suffix + '.bak')
            file_path.rename(backup_path)
            file_path.write_text(modified_content)
            click.echo(f"Saved backup to {backup_path}")
            click.echo(f"Updated {file_path}")
        else:
            click.echo("No changes needed")
            
    def _split_content(self, content: str) -> List[str]:
        """
        Split LaTeX content into processable chunks while preserving structure.
        
        Args:
            content: Full LaTeX content
            
        Returns:
            List of content chunks
        """
        # TODO: Implement smarter splitting that preserves LaTeX environments
        # For now, split by paragraphs
        chunks = re.split(r'\n\s*\n', content)
        return [chunk.strip() + '\n\n' for chunk in chunks if chunk.strip()]
        
    def _get_suggestions(self, chunk: str) -> List[Tuple[str, str]]:
        """
        Get improvement suggestions for a chunk of text from the AI model.
        
        Args:
            chunk: Text chunk to analyze
            
        Returns:
            List of (original, suggestion) pairs
        """
        prompt = f"""
        You are an expert in academic writing and LaTeX. Please suggest improvements 
        to the following LaTeX text to make it more polished and suitable for top 
        scientific conferences. Focus on grammar, style, and clarity while preserving
        all numerical values and LaTeX commands exactly.

        For each suggested change, format your response exactly as follows:
        Original: <text to be replaced>
        Suggestion: <improved text>

        Only suggest changes that meaningfully improve the text. Preserve all LaTeX commands.
        
        TEXT:
        {chunk}
        """
        
        try:
            # Format request body according to Claude's requirements
            request_body = {
                "prompt": prompt,
                "max_tokens_to_sample": 2000,
                "temperature": 0.7,
                "top_p": 1,
                "anthropic_version": "bedrock-2023-05-31"
            }
            
            import json
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body).encode()
            )
            
            # Parse the response
            response_body = json.loads(response.get('body').read().decode())
            completion = response_body.get('completion', '')
            
            # Extract suggestions from completion
            suggestions = []
            lines = completion.strip().split('\n')
            current_original = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('Original:'):
                    current_original = line[9:].strip()
                elif line.startswith('Suggestion:') and current_original:
                    suggestion = line[11:].strip()
                    suggestions.append((current_original, suggestion))
                    current_original = None
                    
            return suggestions
            
        except Exception as e:
            click.echo(f"Error while getting suggestions: {str(e)}", err=True)
            return []
        
    def _apply_suggestions(self, chunk: str, suggestions: List[Tuple[str, str]]) -> str:
        """
        Apply accepted suggestions to a chunk of text.
        
        Args:
            chunk: Original text chunk
            suggestions: List of (original, suggestion) pairs
            
        Returns:
            Modified text chunk
        """
        modified = chunk
        for original, suggestion in suggestions:
            if click.confirm(f"Replace:\n{original}\nwith:\n{suggestion}"):
                modified = modified.replace(original, suggestion)
        return modified



