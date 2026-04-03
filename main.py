#!/usr/bin/env python3
import sys
import os 
import re 

from modules import scan  # add the rest of the modules later 

from modules.httpx import run_httpx


def check_priv():
    # checks if the script is being run with root privileges, if not it exits with a message 
    if os.getuid() != 0:
        print("[-] Please run this script with root privileges.")
        sys.exit(1) 
     
        
def validate(target_ip):
    # inpuit validation
    pattern = r"^[a-zA-Z0-9.-]+$"
    
    # re.match checks if the user's input strictly follows our pattern
    if re.match(pattern, target_ip):
        return True
    else:
        return False


def main():
        
    print("""
    =========================================
    =   Quasly Automated Vulnerability Scanner  :) =
    =========================================
    """)
    
    # 1.1 Security - checking for root privileges 
    check_priv()
    
    target_ip = input("Enter the target IP address or domain name: ").strip() # strip thing gets ris of whitespace from start and end of string
    
    # 1.2  Security  - Checking if its actually a valid IP 
    if not validate(target_ip):
        print("[-] Invalid target IP address or domain name.")
        sys.exit(1)
    
    # 2.1 Rustscan 
    print("--- PHASE 1: Port Discovery (RustScan) ---")
    raw_rustscan_output = scan.rust_scan(target_ip) 
    
    if not raw_rustscan_output:
        print("[-] Pipeline halted: RustScan failed to return data.")
        sys.exit(1)
    
    open_ports = scan.parse_ports(raw_rustscan_output)
    
    # Failsafe: If no ports are open, there's nothing to hack. Stop here.
    if not open_ports:
        print("[-] Pipeline finished: No open ports found on the target.")
        sys.exit(0)
    
    
    # 2.2 httpx   
    print("--- PHASE 2: Web Server Probing (httpx) ---")
    live_urls = run_httpx(target_ip, open_ports)
    
    # Failsafe: If ports are open but none are websites, stop here.
    if not live_urls:
        print("[-] Pipeline finished: No live HTTP/HTTPS web servers found.")
        sys.exit(0)
        
    print(f"\n[+] Pipeline Success! Live URLs ready for the next phase:")
    for url in live_urls:
        print(f"    -> {url}")


if __name__ == "__main__":
    # This prevents main() from running automatically if you ever 
    # import this file into another project later.
    main()