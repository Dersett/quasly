# quasly
Automatic Vulnerability Scanner For Blue Teams
Combination of combine, rust scan, katana, nuclei, nikto and reporting system 

Run These commands

1. First clone the github repo 

        git clone https://github.com/Dersett/quasly 

2. Move to the /opt/ directory 

        sudo mv quasly /opt/quasly
        cd /opt/quasly

3. Run the setup.sh 

        sudo chmod +x setup.sh
        sudo ./setup.sh

4. Create the global command

        sudo ln -s /opt/quasly/main.py /usr/local/bin/quasly

5. Run Quasly and Your Done (Must be in root)

        sudo quasly
