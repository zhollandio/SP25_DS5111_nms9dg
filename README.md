# Chrome Headless & Virtual Environment Setup

## Project Overview

This repository provides a structured way to set up a new VM with a headless Chrome browser for web scraping and data collection. It automates the setup using scripts and a Makefile, allowing new users to get started quickly.

## Table of Contents

1. [VM Bootstrap Sequence](#vm-bootstrap-sequence)
2. [Cloning & Initializing the Project](#cloning--initializing-the-project)
3. [Installing Headless Chrome](#installing-headless-chrome)
4. [Project Setup: Virtual Environment & Dependencies](#project-setup-virtual-environment--dependencies)
5. [Running Headless Chrome Job](#running-headless-chrome-job)
6. [Project Directory Structure](#project-directory-structure)
7. [Summary of Commands](#summary-of-commands)

## VM Bootstrap Sequence

### Prerequisites

Before setting up the project, perform the following manual steps on your new VM:

```bash
sudo apt update
```

### Setting Up Git Credentials & SSH Key

If you haven't set up your Git credentials and SSH key, follow these steps:

1. Set up Git global configuration:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

2. Generate an SSH key (if you haven't already):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

3. Copy and add your SSH key to GitHub/GitLab:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

4. Test your SSH connection:
   ```bash
   ssh -T git@github.com
   ```

## Cloning & Initializing the Project

After setting up your Git credentials, clone this repository:

```bash
git clone <your-repository-url>
cd <your-repository-directory>
```

Then, run the initialization script to set up the VM:

```bash
chmod +x init.sh
./init.sh
```

This script:
- Updates package lists (`sudo apt update`)
- Installs necessary tools: `make`, `python3.12-venv`, and `tree`

## Installing Headless Chrome

To install Google Chrome for headless browsing:

```bash
chmod +x scripts/install_chrome.sh
./scripts/install_chrome.sh
```

Test the installation using:

```bash
google-chrome --headless --disable-gpu --dump-dom https://example.com
```

If it outputs HTML content, Chrome is successfully installed.

## Project Setup: Virtual Environment & Dependencies

### Dependencies

This project requires:
- `pandas`
- `lxml`

These dependencies are listed in `requirements.txt`.

To set up a virtual environment and install dependencies:

```bash
make update
```

This command will:
- Create a Python virtual environment (`env/`)
- Upgrade `pip`
- Install dependencies from `requirements.txt`

## Running Headless Chrome Job

To test the headless browser:

```bash
make ygainers.csv
```

This command:
- Runs headless Chrome
- Fetches the DOM of `https://example.com`
- Saves the output into `sample_data/ygainers.csv`

Check the output file:

```bash
ls -l sample_data/ygainers.csv
```

### Encountered Issues & Fixes

#### Issue: Chrome returns `org.freedesktop.UPower` errors

When running `make ygainers.csv`, you might see errors like:

```bash
google-chrome --headless --disable-gpu --dump-dom https://example.com > sample_data/ygainers.csv
[5301:5383:0205/174912.445271:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.DBus.Properties.Get
[5301:5383:0205/174912.446504:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.UPower.GetDisplayDevice
[5301:5383:0205/174912.448370:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.UPower.EnumerateDevices
```

**Fix:** These errors can be ignored. They occur because Chrome is running on a server without a desktop environment. Chrome is trying to query battery/power status, but this does not affect functionality.

If no `.csv` file is created, check manually:

```bash
google-chrome --headless --disable-gpu --dump-dom https://example.com > sample_data/ygainers.csv
ls -l sample_data/ygainers.csv
```

## Project Directory Structure

View the project structure using:

```bash
tree ~/SP25_DS5111_nms9dg -I env
```

Sample Output:
```
.
├── LICENSE
├── Makefile
├── README.md
├── init.sh
├── requirements.txt
├── scripts
│   └── install_chrome.sh
├── sample_data
│   └── ygainers.csv
└── ssh_config_sample
```

## Summary of Commands

### Setup Commands
```bash
sudo apt update
git clone <your-repo-url>
cd <your-repo-directory>
chmod +x init.sh && ./init.sh
chmod +x scripts/install_chrome.sh && ./scripts/install_chrome.sh
```

### Project-Specific Setup
```bash
make update
make ygainers.csv
ls -l sample_data/ygainers.csv
```
