# CRPF Development Environment

This repository contains the setup and configuration for the CRPF (Central Reserve Police Force) development environment.

## Quick Setup

To set up your development environment, run the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

## What Gets Installed

The setup script will install the following components:

### System Updates
- Updates all system packages to the latest versions

### Docker & Container Tools
- Docker.io
- Docker Compose
- Configures Docker service to start automatically

### Python Development Stack
- Python 3
- pip (Python package manager)
- Virtual environment support
- Required Python libraries:
  - pandas (data manipulation)
  - numpy (numerical computing)
  - scikit-learn (machine learning)
  - matplotlib (plotting)
  - flask (web framework)
  - fastapi (modern web API framework)

### Monitoring & System Tools
- htop (interactive process viewer)
- curl (HTTP client)
- wget (file downloader)

## Manual Installation

If you prefer to install components manually, you can follow these steps:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install Python and required libraries
sudo apt install python3-pip python3-venv -y
pip3 install -r requirements.txt

# Install monitoring tools
sudo apt install htop curl wget -y
```

## Post-Installation

After running the setup script:

1. **Log out and log back in** (or restart your session) for Docker group changes to take effect
2. Verify installations:
   ```bash
   docker --version
   python3 --version
   pip3 list
   ```

## Requirements

- Ubuntu/Debian-based Linux distribution
- sudo privileges
- Internet connection for package downloads