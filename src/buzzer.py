import customtkinter as ctk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import psutil
import threading
import time
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for embedding
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import speedtest
import socket
from datetime import datetime
import logging
import math

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Starting the application...")

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

# Initialize CustomTkinter theme
ctk.set_appearance_mode("dark")  # Options: "dark", "light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class Dial(ctk.CTkCanvas):
    def __init__(self, parent, size=150, max_value=100, label="Metric", **kwargs):
        super().__init__(parent, width=size, height=size, bg="black", highlightthickness=0, **kwargs)
        self.size = size
        self.max_value = max_value
        self.label = label
        self.needle = None
        self.value = 0
        self.draw_dial()

    def draw_dial(self):
        self.create_oval(10, 10, self.size-10, self.size-10, outline="#555", width=2)
        self.create_text(self.size//2, self.size-20, text=self.label, fill="white", font=("Segoe UI", 10))
        self.needle = self.create_line(self.size//2, self.size//2, self.size//2, 20, fill="red", width=2)

    def update_value(self, new_val):
        self.value = new_val
        angle = 270 * (new_val / self.max_value) - 135
        radians = math.radians(angle)
        center = self.size // 2
        length = center - 20
        end_x = center + length * math.cos(radians)
        end_y = center + length * math.sin(radians)
        self.coords(self.needle, center, center, end_x, end_y)

class HealthMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Computer Health Monitor")
        self.geometry("600x600")
        self.resizable(False, False)

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Computer Health Monitor", font=("Segoe UI", 24, "bold"))
        self.title_label.pack(pady=10)

        # Clock
        self.clock_label = ctk.CTkLabel(self, text="--:--:--", font=("Segoe UI", 20))
        self.clock_label.pack(pady=10)

        # CPU Dial
        self.cpu_dial = Dial(self, size=200, max_value=100, label="CPU")
        self.cpu_dial.pack(pady=10)

        # RAM Dial
        self.ram_dial = Dial(self, size=200, max_value=100, label="RAM")
        self.ram_dial.pack(pady=10)

        # CPU Temp Dial
        self.temp_dial = Dial(self, size=200, max_value=100, label="Temp")
        self.temp_dial.pack(pady=10)

        # Network Info
        self.net_label = ctk.CTkLabel(self, text="Network: --", font=("Segoe UI", 16))
        self.net_label.pack(pady=10)

        # Speedtest Button
        self.speedtest_btn = ctk.CTkButton(self, text="Run Speed Test", command=self.run_speedtest_thread)
        self.speedtest_btn.pack(pady=10)

        self.after(500, self.update_stats)
        self.after(500, self.update_clock)

    def update_clock(self):
        now = datetime.now().strftime('%H:%M:%S')
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)

    def update_stats(self):
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        temp = get_cpu_temp()
        try:
            temp_val = float(temp.replace('°C',''))
        except:
            temp_val = 0
        ram_percent = ram.percent

        self.cpu_dial.update_value(cpu)
        self.ram_dial.update_value(ram_percent)
        self.temp_dial.update_value(temp_val)

        self.net_label.config(text=f"Network: {self.get_network_info()}")
        self.after(1000, self.update_stats)

    def get_network_info(self):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return f"Connected ({ip})"
        except Exception:
            return "Disconnected"

    def run_speedtest_thread(self):
        threading.Thread(target=self.run_speedtest, daemon=True).start()

    def run_speedtest(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1e6  # Mbps
            upload = st.upload() / 1e6      # Mbps
            ping = st.results.ping
            self.net_label.config(text=f"Speed: ↓ {download:.1f} Mbps ↑ {upload:.1f} Mbps, Ping: {ping:.0f} ms")
        except Exception as e:
            self.net_label.config(text="Speedtest: Error")

if __name__ == "__main__":
    app = HealthMonitorApp()
    app.mainloop()
