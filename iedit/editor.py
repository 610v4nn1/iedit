"""
Core editing functionality for iedit.
"""

import os
import re
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import yaml

from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.prompt import Confirm

from iedit.bedrock import BedrockClient
from iedit.latex import extract_latex_sections, preserve_numerical_values, restore_numerical_values

console = Console()

class LatexEditor:
    """Main class for editing LaTeX files."""
    
    def __init__(self, model: str = "anthropic.claude-v2", config_path: Optional[str] = None, 
                 auto_apply: bool = False):
        """
        Initialize the LaTeX editor.
        
        Args:
            model: The Amazon Bedrock model to use
            config_path: Path to configuration file
            auto_apply: Whether to apply changes without confirmation
        """
        self.model = model
        self.auto_apply = auto_apply
        self.config = self._load_config(config_path)
        self.bedrock_client = BedrockClient(model=model, config=self.config)
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults."""
        config = {
            "aws_profile": None,  # Use default profile
            "aws_region": "us-east-1",
            "context_lines": 5,  # Number of context lines to show around changes
        }
        
        # Try loading from user config directory if no path specified
        if config_path is None:
            user_config = Path.home() / ".iedit" / "config.yaml"
            if user_config.exists():
                config_path = user_config
        
        # Load config file if it exists
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        config.update(user_config)
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load config file: {e}[/yellow]")
                
        return config
    
    def edit_file(self, file_path: Path) -> None:
        """
        Edit a LaTeX file to improve its form, syntax, and grammar.
        
        Args:
            file_path: Path to the LaTeX file
        """
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Process the file
        new_content = self.process_latex(content)
        
        # Write the changes back to the file
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            console.print(f"[green]Updated {file_path}[/green]")
        else:
            console.print(f"[blue]No changes made to {file_path}[/blue]")
    
    def process_latex(self, content: str) -> str:
        """
        Process LaTeX content to improve form, syntax, and grammar.
        
        Args:
            content: The LaTeX content to process
            
        Returns:
            The improved LaTeX content
        """
        # Extract sections to process them separately
        sections = extract_latex_sections(content)
        
        # Process each section
        for i, section in enumerate(sections):
            # Skip very short sections or those that are likely to be commands/preamble
            if len(section.strip()) < 20 or section.strip().startswith('\\'):
                continue
                
            # Preserve numerical values
            section_with_placeholders, value_map = preserve_numerical_values(section)
            
            # Get improved version from AI
            improved_section = self.get_improved_section(section_with_placeholders)
            
            # Restore numerical values
            if improved_section:
                improved_section = restore_numerical_values(improved_section, value_map)
                
                # Show diff and get confirmation
                if self._confirm_change(section, improved_section):
                    sections[i] = improved_section
        
        # Combine sections back into a single document
        return ''.join(sections)
    
    def get_improved_section(self, section: str) -> Optional[str]:
        """
        Get an improved version of a LaTeX section from the AI model.
        
        Args:
            section: The LaTeX section to improve
            
        Returns:
            The improved section or None if no improvements were suggested
        """
        prompt = f"""
        You are an expert LaTeX editor. Your task is to improve the form, syntax, and grammar of the 
        following LaTeX content while preserving its meaning and all numerical values exactly.
        
        Make the text more professional, clear, and suitable for a top scientific conference.
        Fix any grammatical errors, improve awkward phrasing, and enhance readability.
        
        DO NOT change any mathematical formulas, equations, or the logical structure of the document.
        DO NOT add or remove citations or references.
        DO NOT change the meaning of any sentence.
        
        Return ONLY the improved LaTeX content, without any explanations or comments.
        
        LaTeX content to improve:
        ```
        {section}
        ```
        """
        
        try:
            response = self.bedrock_client.generate_text(prompt)
            
            # Extract the improved content from the response
            improved_section = response.strip()
            
            # If the model wrapped the response in code blocks, remove them
            if improved_section.startswith("```") and improved_section.endswith("```"):
                improved_section = improved_section[3:-3].strip()
                
            # If the model added LaTeX markers, remove them
            if improved_section.startswith("\\begin{document}") and improved_section.endswith("\\end{document}"):
                improved_section = improved_section[16:-14].strip()
                
            return improved_section if improved_section != section else None
            
        except Exception as e:
            console.print(f"[yellow]Warning: Could not get AI suggestions: {e}[/yellow]")
            return None
    
    def _confirm_change(self, original: str, improved: str) -> bool:
        """
        Show the difference between original and improved versions and ask for confirmation.
        
        Args:
            original: The original content
            improved: The improved content
            
        Returns:
            True if the user confirms the change, False otherwise
        """
        if self.auto_apply:
            return True
            
        console.print("\n[bold]Original:[/bold]")
        console.print(Panel(Syntax(original, "latex", theme="monokai")))
        
        console.print("\n[bold]Improved:[/bold]")
        console.print(Panel(Syntax(improved, "latex", theme="monokai")))
        
        return Confirm.ask("Apply this change?", default=True)