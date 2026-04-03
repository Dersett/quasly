# httpx is basically there to give the other tools a url instead of a ip & port
# converts ip and port into url so other tools can process them 
# it also ignores databases and such and only keeps web servers

import subprocess 
import json 


def run_httpx(target_ip, port_list):
    
    # in case where no ports were found by rustscan 
    if not port_list:
        print("No ports provided from scan.py (rustscan)")
        return []
    print(f"Running httpx on {len(port_list)} ports on {target_ip}")
    
    # httpx expects ports in a comma-separated string like "80,443,8080"
    ports_str = ",".join(port_list)
    
    # if using kali linux instead of "httpx" use "httpx-toolkit"
    # sudo apt install httpx-toolkit 
    command = [
        "httpx-toolkit",  # change this to httpx-toolkit if using kali linux else keep httpx 
          # target ip address removed to fix httpx not finding  web servers 
        "-p", ports_str,  # list of ports scanned from rustscan 
        "-silent",  # dont print banners and logos from httpx 
        "-json"  # telling to output in json format    
    ]

    try: 
        outcome = subprocess.run(command, input=target_ip, capture_output=True, text=True, check=True)
        live_urls = [] # added target ip here to fix the issuue of not finding web servers 
        
        # httpx ouptuts one json disctionary per line 
        for line in outcome.stdout.splitlines():
            if line.strip():  # making sure line aint empty
                try:
                    # convert the string toa python dictionary 
                    data = json.loads(line)
                    
                    if "url" in data:
                        live_urls.append(data["url"])
                except json.JSONDecodeError:
                    continue
        
        print(f"[+] httpx found {len(live_urls)} live web servers!")
        return live_urls

    except subprocess.CalledProcessError as e:
        print(f"[-] httpx failed with error: {e.stderr}")
        return []
    except FileNotFoundError:
        print("[-] Unable to locate httpx. Is it installed and in your PATH?")
        return []