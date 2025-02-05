#!/bin/bash
# install_chrome.sh - Chrome for  headless browser usage

echo "Downloading Google Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

echo "Installing Google Chrome..."
sudo apt install -y ./google-chrome-stable_current_amd64.deb

echo "Cleaning up installation files..."
rm google-chrome-stable_current_amd64.deb

echo "Google Chrome installation complete."
