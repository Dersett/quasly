import subprocess 
import re 

# scanning function 
def rust_scan(target_ip):
    print("Starting RustScan on: " + target_ip)
    
    # We use the '-g' flag to get greppable/easier-to-parse output
    # You can add other flags here like '--ulimit 5000' if needed
    command = ["rustscan", "-a", target_ip, "-g"]
    
    # we can make this more optimised by adding a batch size, and ulimit 
            
    try:
        # capture_output=True grabs the terminal text
        # text=True decodes it from bytes to a standard string
        outcome = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # printing out the results 
        print("RustScan completed successfully.")  
        print(outcome.stdout)
        return outcome.stdout 
    
    except subprocess.CalledProcessError as e:
        # This triggers if RustScan runs but returns an error
        print(f"RustScan failed with error: {e.stderr}")
        return None

    except FileNotFoundError: 
        # Gets triggered when rustscan isnt found on the computer 
        print("Unable to locate RustScan, Please ensure RustScan is installed and in your system")
        return None 
    
# extracting ports from raw rustscan text function
def parse_ports(raw_text):
    
    
    print("[*] Parsing output for open ports")
    
    match = re.search(r'\[(.*?)\]', raw_text)
        
    if match:
        ports_string = match.group(1)
        ports_list = ports_string.split(',')
        clean_ports = [port.strip() for port in ports_list if port.strip()]
        return clean_ports
    
    print("[-] No open ports found in the output.")
    return []
