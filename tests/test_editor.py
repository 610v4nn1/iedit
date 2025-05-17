"""
Tests for the LaTeX editor functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import os

from iedit.editor import LatexEditor

class TestLatexEditor(unittest.TestCase):
    """Test the LaTeX editor functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create a sample LaTeX file
        self.sample_latex = r"""
\documentclass{article}
\title{Test Document}
\author{Test Author}
\begin{document}
\maketitle

\section{Introduction}
This is the introduction with some gramatical errors and typos.
The experiment was conducted with 42 participants.

\section{Methods}
These are the methods, which could be writen better.
The accuracy was 95.7\% and the p-value was 0.001.

\end{document}
"""
        self.latex_file = Path(self.temp_dir.name) / "test.tex"
        with open(self.latex_file, 'w') as f:
            f.write(self.sample_latex)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    @patch('iedit.bedrock.BedrockClient')
    @patch('iedit.editor.Confirm.ask')
    def test_edit_file(self, mock_confirm, mock_bedrock_client):
        """Test editing a LaTeX file."""
        # Mock the Bedrock client to return improved text
        mock_instance = mock_bedrock_client.return_value
        mock_instance.generate_text.return_value = r"""
This is the introduction with some grammatical errors and typos corrected.
The experiment was conducted with 42 participants.
"""
        
        # Mock the confirmation to always return True
        mock_confirm.return_value = True
        
        # Create an editor with auto-apply set to False to test confirmation
        editor = LatexEditor(auto_apply=False)
        
        # Process the file
        editor.edit_file(self.latex_file)
        
        # Check that the Bedrock client was called
        mock_instance.generate_text.assert_called()
        
        # Check that confirmation was requested
        mock_confirm.assert_called()
    
    @patch('iedit.bedrock.BedrockClient')
    def test_process_latex(self, mock_bedrock_client):
        """Test processing LaTeX content."""
        # Mock the Bedrock client to return improved text
        mock_instance = mock_bedrock_client.return_value
        mock_instance.generate_text.return_value = r"""
This is the introduction with some grammatical errors and typos corrected.
The experiment was conducted with 42 participants.
"""
        
        # Create an editor with auto-apply set to True to skip confirmation
        editor = LatexEditor(auto_apply=True)
        
        # Process the content
        improved_content = editor.process_latex(self.sample_latex)
        
        # Check that the Bedrock client was called
        mock_instance.generate_text.assert_called()
        
        # Check that the numerical values are preserved
        self.assertIn("42", improved_content)
        self.assertIn("95.7\\%", improved_content)
        self.assertIn("0.001", improved_content)
    
    @patch('iedit.bedrock.BedrockClient')
    def test_get_improved_section(self, mock_bedrock_client):
        """Test getting an improved section from the AI model."""
        # Mock the Bedrock client to return improved text
        mock_instance = mock_bedrock_client.return_value
        mock_instance.generate_text.return_value = "This is the improved text."
        
        # Create an editor
        editor = LatexEditor()
        
        # Get an improved section
        section = "This is the original text."
        improved_section = editor.get_improved_section(section)
        
        # Check that the Bedrock client was called with the correct prompt
        mock_instance.generate_text.assert_called_once()
        prompt = mock_instance.generate_text.call_args[0][0]
        self.assertIn(section, prompt)
        
        # Check that the improved section is returned
        self.assertEqual(improved_section, "This is the improved text.")

if __name__ == '__main__':
    unittest.main()