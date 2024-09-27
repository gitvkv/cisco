Create a YAML file (hosts.yaml) with the list of IP addresses or hostnames.
Create the Python script to read the YAML file, ping the addresses, and generate the report.
--------------------------------

hosts:
  - 8.8.8.8
  - 8.8.4.4
  - example.com
  - 192.168.1.1

--------------------------------     

import subprocess
import yaml
import platform

def load_hosts_from_yaml(file_path):
    """Load hosts from the YAML file."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data.get('hosts', [])

def ping_host(host):
    """Ping a host based on the operating system."""
    # Determine the correct ping command based on OS
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    
    try:
        # Ping the host and capture the output
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return output.returncode == 0  # Return True if ping is successful
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return False

def generate_report(hosts):
    """Generate a report of reachable and unreachable hosts."""
    reachable = []
    unreachable = []

    for host in hosts:
        if ping_host(host):
            reachable.append(host)
        else:
            unreachable.append(host)

    return reachable, unreachable

def main():
    # Path to the YAML file
    yaml_file = 'hosts.yaml'

    # Load hosts from the YAML file
    hosts = load_hosts_from_yaml(yaml_file)

    # Generate the report
    reachable, unreachable = generate_report(hosts)

    # Display the results
    print("\nReachable Hosts:")
    for host in reachable:
        print(f" - {host}")

    print("\nUnreachable Hosts:")
    for host in unreachable:
        print(f" - {host}")

if __name__ == "__main__":
    main()
