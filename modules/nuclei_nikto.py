import subprocess

def run_nuclei(live_urls):
    if not live_urls:
        print("No URLs provided for Nuclei") 
        return []
    
    print(f"[*] Firing Nuclei scanner at {len(live_urls)} base targets. This might take a minute")
    
    # join our URLS to pip them into stdin 
    
    targets_input = "\n".join(live_urls)
    
    command = [
        "nuclei",
        "-silent",
        "-severity", "low,medium,high,critical"
    ]
    
    try:
        outcome = subprocess.run(command, input=targets_input, capture_output= True, text=True, check=True)
        
        findings = []
        for line in outcome.stdout.splitlines():
            clean_line = line.strip()
            if clean_line: 
                findings.append(clean_line) 
                
        return findings
    
    # EXecptions
    except subprocess.CalledProcessError as e:
        print(f"Error running Nuclei: {e}")
        return []       
    except FileNotFoundError:
        print("Nuclei is not installed or not found in PATH. Please install Nuclei and ensure it's in your system's PATH.")
        return []
    
    