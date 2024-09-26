from netmiko import ConnectHandler
import yaml
import getpass

def read_devices_from_yaml(file_path):
    with open(file_path, 'r') as file:
        devices = yaml.safe_load(file)
    return devices['devices']

def execute_commands_on_device(device, username, password, commands):
    try:
        # Set device connection details with keyboard-interactive and password authentication enabled
        device_params = {
            'device_type': device['device_type'],
            'host': device['hostname'],
            'username': username,
            'password': password,
            'fast_cli': False,              # Ensures reliable session handling
            'banner_timeout': 20,           # Handle login prompt delays
            'conn_timeout': 30,             # Timeout for connecting
            'auth_timeout': 20,             # Handles longer authentication times
            'allow_agent': False,           # Disables SSH agent usage
            'use_keys': False,              # Ensures no SSH keys are used
            'global_delay_factor': 2,       # Increases delay for command execution
            'auth_strategy': 'keyboard-interactive', # Sets authentication to keyboard-interactive
        }

        print(f"Connecting to {device['hostname']}...")
        connection = ConnectHandler(**device_params)

        # Save all command outputs to a single file
        with open(f"{device['hostname']}_output.txt", 'w') as file:
            for command in commands:
                output = connection.send_command(command)
                file.write(f"Command: {command}\n")
                file.write(output)
                file.write("\n" + "="*50 + "\n")

        print(f"Outputs from {device['hostname']} saved successfully.")
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect to {device['hostname']}: {str(e)}")

def main():
    yaml_file = 'devices.yaml'
    devices = read_devices_from_yaml(yaml_file)
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    commands = [
        'show version',
        'show ip interface brief',
        'show running-config',
    ]

    for device in devices:
        execute_commands_on_device(device, username, password, commands)

if __name__ == "__main__":
    main()
