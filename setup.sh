#!/bin/bash

# CRPF Development Environment Setup Script
# This script installs Docker, Python, and monitoring tools required for the project

set -e  # Exit on any error

echo "🚀 Starting CRPF development environment setup..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose
echo "🐳 Installing Docker and Docker Compose..."
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install Python and required libraries
echo "🐍 Installing Python and required libraries..."
sudo apt install python3-pip python3-venv -y
pip3 install pandas numpy scikit-learn matplotlib flask fastapi

# Install monitoring tools
echo "📊 Installing monitoring tools..."
sudo apt install htop curl wget -y

echo "✅ Setup completed successfully!"
echo ""
echo "⚠️  Important: Please log out and log back in (or restart your session) for Docker group changes to take effect."
echo "🔍 You can verify Docker installation by running: docker --version"
echo "🐍 You can verify Python installation by running: python3 --version"
echo ""
echo "🎉 Your CRPF development environment is ready!"