import socket
from concurrent.futures import ThreadPoolExecutor


def check_port(ip, port):
    """Attempt to connect to a specific port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    try:
        result = s.connect_ex((ip, port))
        if result == 0:
            return f"Port {port:5} is OPEN"
    except Exception:
        pass
    finally:
        s.close()
    return None


def fast_scan(target_ip, port_range):
    print(f"Fast scanning {target_ip}...\n")

    # max_workers=100 allows 100 threads to run at once
    with ThreadPoolExecutor(max_workers=100) as executor:
        # Map the check_port function across the range of ports
        results = executor.map(lambda p: check_port(target_ip, p), port_range)

        for res in results:
            if res:
                print(res)


# Example usage: Scan ports 1 through 1024
target = "127.0.0.1"
ports_to_scan = range(1, 1025)
fast_scan(target, ports_to_scan)