"""
LaTeX parsing and processing utilities.
"""

import re
from typing import List, Dict, Tuple

def extract_latex_sections(content: str) -> List[str]:
    """
    Extract sections from a LaTeX document for processing.
    
    This function splits a LaTeX document into manageable sections
    while preserving the structure.
    
    Args:
        content: The full LaTeX document content
        
    Returns:
        A list of LaTeX sections
    """
    # Define section markers
    section_markers = [
        r'\\section\{.*?\}',
        r'\\subsection\{.*?\}',
        r'\\subsubsection\{.*?\}',
        r'\\paragraph\{.*?\}',
        r'\\begin\{.*?\}',
        r'\\end\{.*?\}',
    ]
    
    # Combine markers into a single regex pattern
    pattern = '|'.join(section_markers)
    
    # Find all section markers
    matches = list(re.finditer(pattern, content))
    
    if not matches:
        # If no sections found, return the whole document as a single section
        return [content]
    
    # Extract sections
    sections = []
    start_pos = 0
    
    for match in matches:
        # Add text before the marker
        if match.start() > start_pos:
            sections.append(content[start_pos:match.start()])
        
        # Add the marker itself
        sections.append(content[match.start():match.end()])
        start_pos = match.end()
    
    # Add the remaining text
    if start_pos < len(content):
        sections.append(content[start_pos:])
    
    return sections

def preserve_numerical_values(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Replace numerical values with placeholders to preserve them during editing.
    
    Args:
        text: The LaTeX text
        
    Returns:
        A tuple containing:
        - The text with numerical values replaced by placeholders
        - A mapping from placeholders to original values
    """
    # Regular expressions for different numerical formats
    patterns = [
        # Decimal numbers (including scientific notation)
        r'(\d+\.\d+(?:[eE][-+]?\d+)?)',
        # Integer numbers
        r'(\b\d+\b)',
        # LaTeX math expressions with numbers
        r'(\$[^$]*\d+[^$]*\$)',
        # LaTeX equations with numbers
        r'(\\begin\{equation\}.*?\d+.*?\\end\{equation\})',
    ]
    
    value_map = {}
    placeholder_text = text
    
    for pattern in patterns:
        matches = re.finditer(pattern, placeholder_text)
        offset = 0
        
        for match in matches:
            start, end = match.span()
            start += offset
            end += offset
            
            value = placeholder_text[start:end]
            placeholder = f"__NUM_{len(value_map)}__"
            value_map[placeholder] = value
            
            # Replace the value with the placeholder
            placeholder_text = placeholder_text[:start] + placeholder + placeholder_text[end:]
            
            # Adjust offset for subsequent replacements
            offset += len(placeholder) - len(value)
    
    return placeholder_text, value_map

def restore_numerical_values(text: str, value_map: Dict[str, str]) -> str:
    """
    Restore numerical values from placeholders.
    
    Args:
        text: The text with placeholders
        value_map: The mapping from placeholders to original values
        
    Returns:
        The text with original numerical values restored
    """
    result = text
    for placeholder, value in value_map.items():
        result = result.replace(placeholder, value)
    return result