"""
Tests for configuration handling.
"""
import pytest
from pathlib import Path
import yaml
from iedit.config import Config


def test_config_load(tmp_path):
    # Create a test config file
    config_data = {
        'model': 'test-model',
        'options': {
            'backup': True,
            'interactive': True
        }
    }
    
    config_path = tmp_path / 'test_config.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
        
    # Test loading config
    config = Config(str(config_path))
    assert config.get('model') == 'test-model'
    assert config.get('options')['backup'] is True
    
    # Test default value
    assert config.get('nonexistent', 'default') == 'default'