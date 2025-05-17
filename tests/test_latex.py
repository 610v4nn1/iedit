"""
Tests for LaTeX processing functionality.
"""

import unittest
from iedit.latex import extract_latex_sections, preserve_numerical_values, restore_numerical_values

class TestLatexProcessing(unittest.TestCase):
    """Test LaTeX processing functions."""
    
    def test_extract_latex_sections(self):
        """Test extracting sections from LaTeX content."""
        content = r"""
\documentclass{article}
\title{Test Document}
\author{Test Author}
\begin{document}
\maketitle

\section{Introduction}
This is the introduction.

\section{Methods}
These are the methods.

\subsection{Method 1}
Details of method 1.

\begin{equation}
E = mc^2
\end{equation}

\end{document}
"""
        sections = extract_latex_sections(content)
        self.assertGreater(len(sections), 1)
        self.assertIn(r'\section{Introduction}', sections)
        self.assertIn(r'\section{Methods}', sections)
        
    def test_preserve_numerical_values(self):
        """Test preserving numerical values."""
        text = r"""
The experiment was conducted with 42 participants, achieving an accuracy of 95.7%.
The p-value was 0.001, which is statistically significant.
The formula $E = mc^2$ describes the relationship.
\begin{equation}
F = ma
\end{equation}
"""
        placeholder_text, value_map = preserve_numerical_values(text)
        
        # Check that numerical values are replaced
        self.assertNotIn("42", placeholder_text)
        self.assertNotIn("95.7", placeholder_text)
        self.assertNotIn("0.001", placeholder_text)
        
        # Check that placeholders are created
        self.assertGreater(len(value_map), 0)
        
        # Check that values are correctly mapped
        values = list(value_map.values())
        self.assertIn("42", values)
        self.assertIn("95.7%", values)
        self.assertIn("0.001", values)
        
    def test_restore_numerical_values(self):
        """Test restoring numerical values."""
        original_text = "The experiment had 42 participants with 95.7% accuracy."
        placeholder_text, value_map = preserve_numerical_values(original_text)
        restored_text = restore_numerical_values(placeholder_text, value_map)
        
        # Check that the restored text matches the original
        self.assertEqual(original_text, restored_text)
        
    def test_complex_latex_with_numbers(self):
        """Test handling complex LaTeX with numbers."""
        latex_text = r"""
\begin{table}
\caption{Results of the experiment}
\begin{tabular}{|c|c|c|}
\hline
Method & Accuracy & Time (s) \\
\hline
Method 1 & 92.5\% & 0.45 \\
Method 2 & 87.3\% & 0.32 \\
Method 3 & 95.8\% & 0.67 \\
\hline
\end{tabular}
\end{table}
"""
        placeholder_text, value_map = preserve_numerical_values(latex_text)
        restored_text = restore_numerical_values(placeholder_text, value_map)
        
        # Check that all numbers are preserved
        self.assertIn("92.5\\%", restored_text)
        self.assertIn("87.3\\%", restored_text)
        self.assertIn("95.8\\%", restored_text)
        self.assertIn("0.45", restored_text)
        self.assertIn("0.32", restored_text)
        self.assertIn("0.67", restored_text)
        
        # Check that the restored text matches the original
        self.assertEqual(latex_text, restored_text)

if __name__ == '__main__':
    unittest.main()