import subprocess


def run_katana(live_urls):
    
    # making sure we have live urls for katana to process 
    if not live_urls:
        print("No live URLS provided to katana")
        return []
    
    print(f"Running katana on {len(live_urls)}")
    
    targets_inputs = "/n".join(live_urls)
    
    # katana command 
    command = [
        "katana",
        "-silent",
        "-d", "2"
    ]
        
    # running the katana command with subprocess and getting the output 
    try:
        outcome = subprocess.run(command, input=targets_inputs, capture_output=True, text=True, check=True)
        
        crawled_endpoints = []
        
        # parsing the output line by line for a clean output
        for line in outcome.stdout.splitlines():
            clean_line = line.strip()
            if clean_line:
                crawled_endpoints.append(clean_line) 
                
        # Remove any duplicate URLs it might have found
        unique_endpoints = list(set(crawled_endpoints))
        
        # final outoput / printing the endpoints
        print(f"[+] Katana found {len(unique_endpoints)} total endpoints!")
        return unique_endpoints
    
    # exceptions for subprocess errors and file not found errors for katana
    except subprocess.CalledProcessError as e:
        print(f"[-] Katana failed with error: {e.stderr}")
        return []
    except FileNotFoundError:
        print("[-] Unable to locate katana. Is it installed and in your PATH?")
        return []
    