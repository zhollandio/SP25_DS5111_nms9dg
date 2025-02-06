#!/bin/bash
set -o errexit   # abort on nonzero exitstatus

# init.sh - Bootstrap script for VM setup
# Update package index
echo "Updating package index..."
sudo apt update

# install: make, python3.12-venv & tree
echo "Installing required packages: make, python3.12-venv, tree"
sudo apt install -y make python3.12-venv tree

echo "Install complete."
