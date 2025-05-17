"""
Utility functions for iedit.
"""

import os
import re
import tempfile
from pathlib import Path
from typing import List, Optional

def is_latex_file(file_path: Path) -> bool:
    """
    Check if a file is a LaTeX file based on extension and content.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a LaTeX file, False otherwise
    """
    # Check extension
    if file_path.suffix.lower() != '.tex':
        return False
    
    # Check content for LaTeX markers
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(1000)  # Read first 1000 chars
            return '\\documentclass' in content or '\\begin{document}' in content
    except Exception:
        return False

def find_latex_files(directory: Path, recursive: bool = False) -> List[Path]:
    """
    Find all LaTeX files in a directory.
    
    Args:
        directory: Base directory from which the search will start
        recursive: Whether to search recursively
        
    Returns:
        List of paths to LaTeX files
    """
    latex_files = []
    
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.tex'):
                    file_path = Path(root) / file
                    if is_latex_file(file_path):
                        latex_files.append(file_path)
    else:
        for item in directory.iterdir():
            if item.is_file() and item.suffix.lower() == '.tex':
                if is_latex_file(item):
                    latex_files.append(item)
    
    return latex_files

def create_backup(file_path: Path) -> Optional[Path]:
    """
    Create a backup of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Path to the backup file or None if backup failed
    """
    try:
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        with open(file_path, 'r', encoding='utf-8') as src, open(backup_path, 'w', encoding='utf-8') as dst:
            dst.write(src.read())
        return backup_path
    except Exception:
        return None

def restore_backup(backup_path: Path) -> bool:
    """
    Restore a file from its backup.
    
    Args:
        backup_path: Path to the backup file
        
    Returns:
        True if restoration was successful, False otherwise
    """
    try:
        original_path = backup_path.with_suffix('')
        with open(backup_path, 'r', encoding='utf-8') as src, open(original_path, 'w', encoding='utf-8') as dst:
            dst.write(src.read())
        return True
    except Exception:
        return False