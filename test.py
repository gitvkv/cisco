import socket
import ipaddress

def get_hostnames_from_subnet(subnet):
    try:
        # Create an IPv4 network object
        network = ipaddress.IPv4Network(subnet, strict=False)
        hostnames = {}
        
        # Iterate over all IP addresses in the subnet
        for ip in network.hosts():
            try:
                # Get the hostname for each IP
                hostname = socket.gethostbyaddr(str(ip))[0]
            except socket.herror:
                hostname = "Unresolved"
            hostnames[str(ip)] = hostname
        return hostnames
    except ValueError as e:
        return f"Invalid subnet: {e}"

# Example usage
subnet = "192.168.1.0/24"  # Replace with your subnet
hostnames = get_hostnames_from_subnet(subnet)

for ip, hostname in hostnames.items():
    print(f"{ip}: {hostname}")
