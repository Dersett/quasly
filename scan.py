import subprocess 

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
        return outcome.stdout 
    
    except subprocess.CalledProcessError as e:
        # This triggers if RustScan runs but returns an error
        print(f"RustScan failed with error: {e.stderr}")
        return None

    except FileNotFoundError: 
        # Gets triggered when rustscan isnt found on the computer 
        print("Unable to locate RustScan, Please ensure RustScan is installed and in your system")
        return None 
    
# --- Testing the function --- Delete later becuase we will be making a main.py which will call all the function including this and then also need to 
# make main one to work like a command line tool where you can specify the target and the scan type and then it will call the appropriate function and then print the results in a nice format.
if __name__ == "__main__":
    
    target = "127.0.0.1" # Replace with your test target
    raw_output = rust_scan(target)
    
    if raw_output:
        print("\n--- Raw Output ---")
        print(raw_output)
    