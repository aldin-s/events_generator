#!/bin/bash

# Check if virtualenv is installed, if not, install it
if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv could not be found, installing..."
    pip3 install virtualenv
fi

# Create a virtual environment named 'venv' with Python 3
virtualenv -p python3 venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages from requirements.txt
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found!"
fi

# Deactivate the virtual environment
deactivate

echo "Setup complete. Virtual environment 'venv' created and requirements installed."
