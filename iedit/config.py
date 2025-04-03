"""
Configuration handling for iedit.
"""
from pathlib import Path
from typing import Optional, Dict, Any
import yaml


class Config:
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration, optionally loading from a file.
        
        Args:
            config_path: Optional path to YAML configuration file
        """
        self.config: Dict[str, Any] = {}
        
        if config_path:
            self.load_config(config_path)
        else:
            # Try default locations
            default_locations = [
                Path.home() / '.config' / 'iedit' / 'config.yaml',
                Path.home() / '.iedit.yaml',
            ]
            
            for path in default_locations:
                if path.exists():
                    self.load_config(str(path))
                    break
                    
    def load_config(self, path: str) -> None:
        """
        Load configuration from a YAML file.
        
        Args:
            path: Path to configuration file
        """
        with open(path) as f:
            self.config = yaml.safe_load(f)
            
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)