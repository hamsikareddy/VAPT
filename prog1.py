import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor

def ping_host(ip):
    """Pings a single host and returns the IP if alive, else None"""
    # Use lowercase 'param' to match the next line
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return ip
    except Exception:
        pass
    return None

def ping_sweep(network_prefix, threads=50):
    """Performs a ping sweep on a /24 network"""
    print(f"Starting ping sweep on {network_prefix}.0/24\n")
    live_hosts = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        ips = [f"{network_prefix}.{i}" for i in range(1, 255)]
        # list() ensures the map finishes before moving to the loop
        results = list(executor.map(ping_host, ips))

    for host in results:
        if host:
            print(f"[+] Host alive: {host}")
            live_hosts.append(host)

    print("\nPing sweep complete.")
    print(f"Live hosts found: {len(live_hosts)}")
    return live_hosts

if __name__ == "__main__":
    ping_sweep("192.168.1")