#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing project..."
pip install -e .

echo "Rebooting the virtual environment..."
deactivate
source venv/bin/activate
