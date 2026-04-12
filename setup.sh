#!/bin/bash

echo "========================================="
echo "=   Installing Quasly Dependencies :    ="
echo "========================================="

# 1. Update package lists
echo "[*] Updating apt repositories"
sudo apt update -y

# 2. Install httpx-toolkit from Kali repositories
echo "[*] Installing httpx-toolkit"
sudo apt install httpx-toolkit -y

# 3. Install dos2unix (to prevent Windows formatting errors)
echo "[*] Installing dos2unix"
sudo apt install dos2unix -y


# 4. Check for RustScan
echo "[*] Checking for RustScan..."
if ! command -v rustscan &> /dev/null
then
    echo "[!] RustScan not found. Downloading and installing now"
    
    # Download the .deb file quietly (-q) so it doesn't spam the terminal
    wget -q https://github.com/RustScan/RustScan/releases/download/2.1.1/rustscan_2.1.1_amd64.deb
    
    # Install the package
    sudo dpkg -i rustscan_2.1.1_amd64.deb
    
    # Clean up the downloaded file so we don't leave trash behind
    rm rustscan_2.1.1_amd64.deb
    
    echo "[+] RustScan successfully installed!"
else
    echo "[+] RustScan is already installed!"
fi

# 5 Installing Katana
# depending on the system os, you may need to set up the GOPATH and PATH variables for Go. 
echo 'export GOPATH=$HOME/go' >> ~/.zshrc
echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.zshrc
source ~/.zshrc
echo "installing golang-go (required for Katana)"
sudo apt install golang-go -y
echo "[*] Installing Katana"
sudo apt install katana -y

echo "========================================="
echo "=        Installation Complete! :)      ="
echo "========================================="