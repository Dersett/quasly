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

# 5. Installing Katana and Go environment
echo "[*] Setting up Golang environment variables..."
echo 'export GOPATH=$HOME/go' >> ~/.zshrc
echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.zshrc

echo "[*] Installing golang-go..."
sudo apt install golang-go -y

echo "[*] Installing Katana crawler..."
sudo apt install katana -y

# 6. Installing Nuclei & Advanced Dependencies
echo "[*] Installing Nuclei and advanced modules (unzip, chromium, libpcap)..."
sudo apt install nuclei unzip chromium libpcap-dev -y

echo "[*] Initializing Nuclei and downloading the latest vulnerability templates..."
# This pulls the massive library of attack signatures down to the user's machine
nuclei -update-templates

echo "========================================="
echo "=        Installation Complete! :)      ="
echo "========================================="
echo ""
echo "[!] IMPORTANT: Please close this terminal and open a new one,"
echo "    OR run 'source ~/.zshrc' before running Quasly for the first time."