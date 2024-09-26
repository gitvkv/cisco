from netmiko import ConnectHandler
import yaml
import getpass

# Function to read device details from YAML file
def read_devices_from_yaml(file_path):
    with open(file_path, 'r') as file:
        devices = yaml.safe_load(file)
    return devices['devices']

# Function to execute multiple commands on a device using Netmiko
def execute_commands_on_device(device, username, password, commands):
    try:
        # Setting up device connection details
        device_params = {
            'device_type': device['device_type'],
            'host': device['hostname'],
            'username': username,
            'password': password,
            'disable_host_key_checking': True,
        }

        # Connecting to the device
        print(f"Connecting to {device['hostname']}...")
        connection = ConnectHandler(**device_params)

        # Opening a single file to store all command outputs for this device
        with open(f"{device['hostname']}_output.txt", 'w') as file:
            for command in commands:
                # Sending the command
                output = connection.send_command(command)
                
                # Saving the command output to the file
                file.write(f"Command: {command}\n")
                file.write(output)
                file.write("\n" + "="*50 + "\n")  # Separator for readability

        print(f"Outputs from {device['hostname']} saved successfully.")
        
        # Closing the connection
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect to {device['hostname']}: {str(e)}")

# Main function
def main():
    # Getting the YAML file path
    yaml_file = 'devices.yaml'

    # Reading devices from YAML
    devices = read_devices_from_yaml(yaml_file)

    # Asking for username and password once
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # List of commands to be executed on each device
    commands = [
        'show version',      # Add more commands as needed
        'show ip interface brief',
        'show running-config',
        # Add more commands as required
    ]

    # Looping through each device and executing the commands
    for device in devices:
        execute_commands_on_device(device, username, password, commands)

if __name__ == "__main__":
    main()
