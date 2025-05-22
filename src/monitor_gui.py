import ttkbootstrap as tb
from ttkbootstrap.constants import *
import psutil
import socket
from datetime import datetime, timedelta

# Helper functions
def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                if 'cpu' in entry.label.lower() or 'core' in entry.label.lower():
                    return f"{entry.current:.1f}°C"
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

def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        if battery:
            plugged = 'Plugged In' if battery.power_plugged else 'On Battery'
            return f"{battery.percent:.1f}% ({plugged})"
    except Exception:
        pass
    return "N/A"

def get_uptime():
    boot = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    delta = now - boot
    return str(timedelta(seconds=int(delta.total_seconds())))

class MonitorGUI(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("System Monitor")
        self.geometry("440x340")
        self.resizable(False, False)

        style = tb.Style()
        style.configure('Stat.TLabel', font=("Segoe UI", 12, "bold"), foreground="#00d4ff")
        style.configure('Value.TLabel', font=("Segoe UI", 12), foreground="#fff")

        self.frame = tb.Frame(self, padding=20)
        self.frame.pack(fill=tb.BOTH, expand=True)

        self.labels = {}
        row = 0
        for label in [
            "Time", "Uptime", "CPU Usage", "RAM Usage", "CPU Temp", "Disk Usage", "Net Up", "Net Down", "Network", "Battery"]:
            l = tb.Label(self.frame, text=label+":", style='Stat.TLabel', anchor="w")
            l.grid(row=row, column=0, sticky="w", padx=(0,10), pady=4)
            v = tb.Label(self.frame, text="--", style='Value.TLabel', anchor="w")
            v.grid(row=row, column=1, sticky="w", padx=10, pady=4)
            self.labels[label] = v
            row += 1

        self.last_bytes_sent = psutil.net_io_counters().bytes_sent
        self.last_bytes_recv = psutil.net_io_counters().bytes_recv
        self.after(500, self.update_stats)

    def update_stats(self):
        now = datetime.now().strftime('%H:%M:%S')
        self.labels["Time"].config(text=now)
        self.labels["Uptime"].config(text=get_uptime())
        self.labels["CPU Usage"].config(text=f"{psutil.cpu_percent():.1f}%")
        self.labels["RAM Usage"].config(text=f"{psutil.virtual_memory().percent:.1f}%")
        self.labels["CPU Temp"].config(text=get_cpu_temp())
        disk = psutil.disk_usage('/')
        self.labels["Disk Usage"].config(text=f"{disk.percent:.1f}%")
        net = psutil.net_io_counters()
        up = (net.bytes_sent - self.last_bytes_sent) / 1024  # KB
        down = (net.bytes_recv - self.last_bytes_recv) / 1024  # KB
        self.labels["Net Up"].config(text=f"{up:.1f} KB/s")
        self.labels["Net Down"].config(text=f"{down:.1f} KB/s")
        self.last_bytes_sent = net.bytes_sent
        self.last_bytes_recv = net.bytes_recv
        self.labels["Network"].config(text=get_network_info())
        self.labels["Battery"].config(text=get_battery_info())
        self.after(1000, self.update_stats)

if __name__ == "__main__":
    app = MonitorGUI()
    app.mainloop()
