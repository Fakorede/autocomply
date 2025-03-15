#!/bin/bash

# Install dependencies
python3 -m pip install git+https://github.com/appknox/pyaxmlparser.git
python3 -m pip install androguard==3.3.5

# Grant execute permissions to the script
chmod +x car_feat.py

echo "Setup completed successfully!"
