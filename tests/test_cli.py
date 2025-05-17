"""
Tests for the command-line interface.
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import os
import sys

from click.testing import CliRunner
from iedit.cli import main

class TestCLI(unittest.TestCase):
    """Test the command-line interface."""
    
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
This is the introduction.

\section{Methods}
These are the methods.

\end{document}
"""
        self.latex_file = Path(self.temp_dir.name) / "test.tex"
        with open(self.latex_file, 'w') as f:
            f.write(self.sample_latex)
        
        # Create a directory with multiple LaTeX files
        self.latex_dir = Path(self.temp_dir.name) / "latex_dir"
        self.latex_dir.mkdir()
        
        for i in range(3):
            with open(self.latex_dir / f"test{i}.tex", 'w') as f:
                f.write(self.sample_latex)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    @patch('iedit.editor.LatexEditor')
    def test_process_file(self, mock_editor_class):
        """Test processing a single file."""
        # Mock the editor
        mock_editor = mock_editor_class.return_value
        
        # Run the CLI
        runner = CliRunner()
        result = runner.invoke(main, [str(self.latex_file)])
        
        # Check that the command ran successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the editor was created with the default model
        mock_editor_class.assert_called_once_with(
            model='anthropic.claude-v2', 
            config_path=None, 
            auto_apply=False
        )
        
        # Check that the file was processed
        mock_editor.edit_file.assert_called_once_with(self.latex_file)
    
    @patch('iedit.editor.LatexEditor')
    def test_process_directory(self, mock_editor_class):
        """Test processing a directory."""
        # Mock the editor
        mock_editor = mock_editor_class.return_value
        
        # Run the CLI
        runner = CliRunner()
        result = runner.invoke(main, [str(self.latex_dir)])
        
        # Check that the command ran successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the editor was created
        mock_editor_class.assert_called_once()
        
        # Check that edit_file was called for each file
        self.assertEqual(mock_editor.edit_file.call_count, 3)
    
    @patch('iedit.editor.LatexEditor')
    def test_custom_model(self, mock_editor_class):
        """Test specifying a custom model."""
        # Mock the editor
        mock_editor = mock_editor_class.return_value
        
        # Run the CLI with a custom model
        runner = CliRunner()
        result = runner.invoke(main, ['--model', 'amazon.titan-text-express-v1', str(self.latex_file)])
        
        # Check that the command ran successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the editor was created with the specified model
        mock_editor_class.assert_called_once_with(
            model='amazon.titan-text-express-v1', 
            config_path=None, 
            auto_apply=False
        )
    
    @patch('iedit.editor.LatexEditor')
    def test_auto_apply(self, mock_editor_class):
        """Test auto-apply option."""
        # Mock the editor
        mock_editor = mock_editor_class.return_value
        
        # Run the CLI with auto-apply
        runner = CliRunner()
        result = runner.invoke(main, ['--yes', str(self.latex_file)])
        
        # Check that the command ran successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the editor was created with auto_apply=True
        mock_editor_class.assert_called_once_with(
            model='anthropic.claude-v2', 
            config_path=None, 
            auto_apply=True
        )
    
    @patch('iedit.bedrock.get_available_models')
    def test_list_models(self, mock_get_models):
        """Test listing available models."""
        # Mock the get_available_models function
        mock_get_models.return_value = [
            'anthropic.claude-v2',
            'amazon.titan-text-express-v1',
        ]
        
        # Run the CLI with --list-models
        runner = CliRunner()
        result = runner.invoke(main, ['--list-models'])
        
        # Check that the command ran successfully
        self.assertEqual(result.exit_code, 0)
        
        # Check that the models are listed in the output
        self.assertIn('anthropic.claude-v2', result.output)
        self.assertIn('amazon.titan-text-express-v1', result.output)

if __name__ == '__main__':
    unittest.main()