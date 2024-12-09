import ipaddress
import subprocess

def ping_host(ip):
    try:
        # Use subprocess to ping the IP
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", str(ip)],  # Windows-specific ping command
            stdout=subprocess.DEVNULL,  # Suppress output
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0  # Return True if ping was successful
    except Exception as e:
        return False

def check_reachability(subnet):
    try:
        # Create an IPv4 network object
        network = ipaddress.IPv4Network(subnet, strict=False)
        reachability = {}
        
        # Iterate over all hosts in the subnet
        for ip in network.hosts():
            is_reachable = ping_host(ip)
            reachability[str(ip)] = "Reachable" if is_reachable else "Unreachable"
        
        return reachability
    except ValueError as e:
        return f"Invalid subnet: {e}"

# Example usage
subnet = "192.168.1.0/24"  # Replace with your subnet
reachability_status = check_reachability(subnet)

for ip, status in reachability_status.items():
    print(f"{ip}: {status}")
