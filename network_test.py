import socket
import subprocess
import platform

def get_host_info(hostname):
    """Get IP address for a hostname"""
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        return None

def get_local_info():
    """Get local hostname and IP"""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return hostname, ip

def is_reachable_ping(hostname):
    """Check reachability using ping"""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', hostname]
    
    try:
        if platform.system().lower() == 'windows':
            command.extend(['-w', '3000'])
        else:
            command.extend(['-W', '3'])
        
        result = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result == 0
    except:
        return False

def is_reachable_socket(hostname, port=80, timeout=3):
    """Check reachability using socket connection"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((hostname, port))
        sock.close()
        return result == 0
    except:
        return False

# --- Main Program ---
print("=" * 60)
print(" NETWORK REACHABILITY TESTER")
print("=" * 60)

# 1. Resolve hostnames
print("\n1. HOSTNAME RESOLUTION:")
print("-" * 40)
test_hosts = ["www.google.com", "www.python.org", "www.github.com"]

for host in test_hosts:
    ip = get_host_info(host)
    if ip:
        print(f"  {host:25} -> {ip}")
    else:
        print(f"  {host:25} -> NOT FOUND")

# 2. Local host info
print("\n2. LOCAL HOST INFORMATION:")
print("-" * 40)
hostname, local_ip = get_local_info()
print(f"  Hostname:   {hostname}")
print(f"  IP Address: {local_ip}")

# 3. Reachability testing (Ping)
print("\n3. REACHABILITY TESTING (PING):")
print("-" * 40)

for host in test_hosts:
    print(f"  Testing {host}:", end=" ")
    ping_ok = is_reachable_ping(host)
    print(f"{'✓ REACHABLE' if ping_ok else '✗ NOT REACHABLE'}")

# 4. Reachability testing (Socket)
print("\n4. REACHABILITY TESTING (SOCKET - HTTP Port 80):")
print("-" * 40)

for host in test_hosts:
    print(f"  Testing {host}:", end=" ")
    socket_ok = is_reachable_socket(host, 80)
    print(f"{'✓ PORT 80 OPEN' if socket_ok else '✗ PORT 80 CLOSED/FILTERED'}")

print("\n" + "=" * 60)
print(" TEST COMPLETE")
print("=" * 60)