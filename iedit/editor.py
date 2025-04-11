"""
Core LaTeX editing functionality
"""
import re
import boto3
import click
from typing import List, Tuple, Optional

class LatexEditor:
    def __init__(self, model: str, **kwargs):
        """
        Initialize the LaTeX editor.
        
        Args:
            model: The Bedrock model to use
            **kwargs: Additional configuration options
        """
        self.model = model
        self.bedrock = boto3.client('bedrock-runtime')
        
    def process_file(self, filepath: str) -> None:
        """
        Process a single LaTeX file, suggesting and applying improvements.
        
        Args:
            filepath: Path to the LaTeX file to process
        """
        with open(filepath, 'r') as f:
            content = f.read()
            
        chunks = self._split_content(content)
        modified_content = content
        
        for chunk in chunks:
            suggestions = self._get_suggestions(chunk)
            if suggestions:
                for original, suggested in suggestions:
                    if self._confirm_change(original, suggested):
                        modified_content = modified_content.replace(original, suggested)
        
        if modified_content != content:
            self._save_changes(filepath, modified_content)
    
    def _split_content(self, content: str) -> List[str]:
        """
        Split the LaTeX content into manageable chunks for processing.
        Preserves LaTeX environments and ensures context is maintained.
        """
        # Simple splitting by paragraphs for now
        # TODO: Implement more sophisticated splitting that respects LaTeX environments
        chunks = re.split(r'\n\s*\n', content)
        return [chunk.strip() for chunk in chunks if chunk.strip()]
    
    def _get_suggestions(self, text: str) -> List[Tuple[str, str]]:
        """
        Get improvement suggestions from Bedrock for a chunk of text.
        
        Args:
            text: The text chunk to improve
            
        Returns:
            List of (original, suggested) text pairs
        """
        prompt = f"""
        Please improve the following LaTeX text for clarity, grammar, and style.
        Preserve all numerical values and LaTeX commands exactly.
        Only suggest changes if they significantly improve the text.
        
        Text:
        {text}
        
        Return only the improved version if changes are needed, otherwise return NONE.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId=self.model,
                body=prompt.encode()
            )
            suggestion = response['body'].decode().strip()
            
            if suggestion and suggestion != "NONE" and suggestion != text:
                return [(text, suggestion)]
            return []
            
        except Exception as e:
            click.echo(f"Warning: Failed to get suggestions: {str(e)}", err=True)
            return []
    
    def _confirm_change(self, original: str, suggested: str) -> bool:
        """
        Ask the user to confirm a suggested change.
        
        Args:
            original: Original text
            suggested: Suggested improvement
            
        Returns:
            True if the user confirms the change, False otherwise
        """
        click.echo("\nOriginal:")
        click.echo(original)
        click.echo("\nSuggested:")
        click.echo(suggested)
        return click.confirm("Apply this change?")
    
    def _save_changes(self, filepath: str, content: str) -> None:
        """
        Save the modified content back to the file.
        
        Args:
            filepath: Path to the file
            content: New content to save
        """
        backup_path = filepath + '.bak'
        # Create backup
        with open(filepath, 'r') as f:
            with open(backup_path, 'w') as backup:
                backup.write(f.read())
                
        # Save new content
        with open(filepath, 'w') as f:
            f.write(content)
            
        click.echo(f"Changes saved to {filepath} (backup created at {backup_path})")