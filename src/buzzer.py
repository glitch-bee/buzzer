import psutil
import speedtest
import socket
import time
from datetime import datetime

# Try to get temperature sensors (may not be available on all systems)
def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                if 'cpu' in entry.label.lower() or 'core' in entry.label.lower():
                    return f"{entry.current:.1f}°C"
        # If no label, just return the first available
        for entries in temps.values():
            if entries:
                return f"{entries[0].current:.1f}°C"
    except Exception:
        pass
    return "N/A"

def get_network_info():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return f"Connected ({ip})"
    except Exception:
        return "Disconnected"

def print_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    temp = get_cpu_temp()
    net = get_network_info()
    now = datetime.now().strftime('%H:%M:%S')
    print(f"[{now}] CPU: {cpu:5.1f}% | RAM: {ram:5.1f}% | Temp: {temp:>6} | {net}")

def run_speedtest():
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1e6  # Mbps
    upload = st.upload() / 1e6      # Mbps
    ping = st.results.ping
    print(f"Speed: ↓ {download:.1f} Mbps ↑ {upload:.1f} Mbps, Ping: {ping:.0f} ms")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple Computer Health Monitor (CLI)")
    parser.add_argument('--speedtest', action='store_true', help='Run a speed test and exit')
    parser.add_argument('--interval', type=float, default=1.0, help='Stats update interval in seconds (default: 1)')
    args = parser.parse_args()

    if args.speedtest:
        run_speedtest()
    else:
        print("Press Ctrl+C to exit.")
        try:
            while True:
                print_stats()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nExiting.")