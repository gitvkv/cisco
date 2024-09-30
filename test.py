import paramiko
import logging
import yaml
import os
import time

# Function to load devices from a YAML file
def load_devices_from_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to execute commands on a switch
def execute_commands_on_switch(hostname, username, password, enable_password, commands):
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the switch
        client.connect(hostname, username=username, password=password)
        logging.info(f"Connected to {hostname}")

        # Open an interactive shell
        shell = client.invoke_shell()
        
        # Enter enable mode
        shell.send('enable\n')
        shell.send(enable_password + '\n')  # Send enable password
        
        # Wait for the shell to be ready
        time.sleep(1)
        
        output = ""
        
        # Execute each command
        for command in commands:
            shell.send(command + '\n')
            time.sleep(1)  # Wait for command execution
            
            # Read output
            output += shell.recv(65535).decode()  # Append command output

        # Log the output to a file
        device_name = hostname.replace('.', '_')  # Replace dots for filename
        output_file = f"{device_name}_output.log"
        
        with open(output_file, 'w') as f:
            f.write(output)
        
        logging.info(f"Output saved to {output_file}")

    except Exception as e:
        logging.error(f"Failed to connect to {hostname}: {e}")
    finally:
        client.close()
        logging.info(f"Connection to {hostname} closed.")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(filename='switch_output.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Load devices from YAML file
    devices = load_devices_from_yaml('devices.yaml')['devices']
    
    # Prompt for username, password, and enable password
    switch_username = input("Enter username: ")
    switch_password = input("Enter password: ")
    enable_password = input("Enter enable password: ")

    # Commands to execute
    commands_to_execute = [
        'show version',
        'show ip interface brief',
        'show running-config'
    ]  # Replace with your desired commands

    for device in devices:
        hostname = device['hostname']
        logging.info(f"Processing {hostname}")
        
        # Execute the commands on the switch
        execute_commands_on_switch(hostname, switch_username, switch_password, enable_password, commands_to_execute)
