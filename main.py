#!/usr/bin/env python3
import sys
import os 
import re 

from modules import scan  # add the rest of the modules later 
from modules.httpx import run_httpx
from modules.katana import run_katana
from modules.nuclei_nikto import run_nuclei

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
        
    # 3.1 Katana
    print("\nPHASE 3: Katana Crawling")
    all_endpoints = run_katana(live_urls)

    if not all_endpoints:
        print("[-] Pipeline finished: Could not crawl any endpoints.")
        sys.exit(0)
        
    print(f"\n[+] Pipeline Success! Here is a sample of discovered endpoints:")
    
    # Print just the first 10 so we don't flood the terminal screen
    for endpoint in all_endpoints[:10]:
        print(f"    -> {endpoint}")
        
    if len(all_endpoints) > 10:
        print(f"    ... and {len(all_endpoints) - 10} more.")

    # 4.1 Nuclei (make sure the katana output is there have all output of each module specified)
    # --- SCAN PROFILE SELECTION ---
    print("=========================================")
    print("=      Select Nuclei Scan Profile   :)  =")
    print("=========================================")
    print("[1] Fast Scan (Base URLs only - Recommended)")
    print("[2] Deep Scan (All Katana Endpoints - Very Slow)")
    print("[3] Custom Scan (Provide specific URLs manually)")
    
    scan_choice = input("\nSelect an option [1/2/3]: ").strip()
    
    nuclei_targets = live_urls # Default to Fast Scan
    
    
    if scan_choice == "2":
        if all_endpoints:
            nuclei_targets = all_endpoints
            print(f"[*] Deep Scan initialized. Targeting {len(nuclei_targets)} endpoints...")
        else:
            print("[-] Katana didn't find extra endpoints. Falling back to Fast Scan.")
    elif scan_choice == "3":
        custom_input = input("\nEnter custom URLs (separated by commas): ").strip()
        nuclei_targets = [url.strip() for url in custom_input.split(",") if url.strip()]
        print(f"[*] Custom Scan initialized. Targeting {len(nuclei_targets)} custom URLs...")
    else:
        print(f"[*] Fast Scan initialized. Targeting {len(nuclei_targets)} base URLs...")
        
        
    # nuclei execution 
    print("\n--- PHASE 4: Vulnerability Scanning (Nuclei) ---")
    findings = run_nuclei(nuclei_targets)
    
    if not findings:
        print("[+] Target looks secure. No vulnerabilities found by Nuclei.")
    else:
        print(f"[!] Found {len(findings)} potential vulnerabilities!")
        for finding in findings:
            print(f"    -> {finding}")

if __name__ == "__main__":
    # This prevents main() from running automatically if you ever 
    # import this file into another project later.
    main()
    
    
