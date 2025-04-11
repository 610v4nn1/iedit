"""
Configuration handling for iedit
"""
import os
import yaml
from typing import Dict, Any

def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the config file. If None, looks for .iedit.yaml in the home directory
        
    Returns:
        Dictionary containing configuration options
    """
    if not config_path:
        config_path = os.path.expanduser('~/.iedit.yaml')
        
    if not os.path.exists(config_path):
        return {}
        
    with open(config_path, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid config file: {str(e)}")