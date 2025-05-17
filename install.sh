#!/bin/bash
# Simple installation script for iedit

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install the package in development mode
echo "Installing iedit in development mode..."
pip install -e .

# Create config directory
mkdir -p ~/.iedit

# Copy example config if it doesn't exist
if [ ! -f ~/.iedit/config.yaml ]; then
    echo "Creating example configuration file..."
    cp config_example.yaml ~/.iedit/config.yaml
fi

echo "Installation complete!"
echo "You can now use iedit by running: iedit --help"