from netmiko import ConnectHandler
import yaml
import getpass

# Function to read device details from YAML file
def read_devices_from_yaml(file_path):
    with open(file_path, 'r') as file:
        devices = yaml.safe_load(file)
    return devices['devices']

# Function to execute command on a device using Netmiko
def execute_command_on_device(device, username, password, command):
    try:
        # Setting up device connection details
        device_params = {
            'device_type': device['device_type'],
            'host': device['hostname'],
            'username': username,
            'password': password,
        }

        # Connecting to the device
        print(f"Connecting to {device['hostname']}...")
        connection = ConnectHandler(**device_params)
        
        # Sending the command
        output = connection.send_command(command)
        
        # Saving the output to a file
        with open(f"{device['hostname']}_output.txt", 'w') as file:
            file.write(output)
        
        print(f"Output from {device['hostname']} saved successfully.")
        
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

    # Command to be executed on the device
    command = 'show version'  # Modify this command as per your requirement

    # Looping through each device and executing the command
    for device in devices:
        execute_command_on_device(device, username, password, command)

if __name__ == "__main__":
    main()
