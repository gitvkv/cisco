import paramiko
import logging
import yaml

# Configure logging
logging.basicConfig(filename='switch_output.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_devices_from_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def execute_command_on_switch(hostname, username, password, command):
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the switch
        client.connect(hostname, username=username, password=password)
        logging.info(f"Connected to {hostname}")

        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)
        
        # Read output and errors
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        # Log the output
        if output:
            logging.info(f"Output from {hostname}:\n{output}")
        if error:
            logging.error(f"Error from {hostname}:\n{error}")

    except Exception as e:
        logging.error(f"Failed to connect to {hostname}: {e}")
    finally:
        client.close()
        logging.info(f"Connection to {hostname} closed.")

if __name__ == "__main__":
    # Load devices from YAML file
    devices = load_devices_from_yaml('devices.yaml')['devices']
    
    # Prompt for username and password
    switch_username = input("Enter username: ")
    switch_password = input("Enter password: ")

    # Command to execute
    command_to_execute = 'show version'  # Replace with your desired command

    for device in devices:
        hostname = device['hostname']
        name = device['name']
        logging.info(f"Processing {name} ({hostname})")
        
        # Execute the command on the switch
        execute_command_on_switch(hostname, switch_username, switch_password, command_to_execute)
