# Computer Health Monitor

## Overview
The **Computer Health Monitor** is a desktop application built using Python and `CustomTkinter`. It provides real-time monitoring of system metrics such as CPU usage, RAM usage, and CPU temperature. The application also includes additional features like a clock, network information display, and a speed test utility.

## Features
- **Real-Time Monitoring**:
  - CPU usage displayed on a custom dial.
  - RAM usage displayed on a custom dial.
  - CPU temperature displayed on a custom dial.
- **Network Information**:
  - Displays the current network status and IP address.
  - Includes a speed test feature to measure download and upload speeds, as well as ping.
- **Clock**:
  - Displays the current time, updated every second.

## Technologies Used
- **Python**: The core programming language.
- **CustomTkinter**: For creating a modern and visually appealing user interface.
- **Psutil**: For retrieving system metrics like CPU and RAM usage.
- **Speedtest-cli**: For performing network speed tests.
- **Socket**: For fetching network information.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/glitch-bee/buzzer.git
   cd buzzer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
   python src/buzzer.py
   ```
2. The application window will display:
   - CPU, RAM, and temperature dials.
   - Current time.
   - Network information.
   - A button to perform a speed test.

## File Structure
- `src/buzzer.py`: The main application file containing all logic and UI components.

## Future Enhancements
- Add support for additional metrics like GPU usage, storage, or fan speed.
- Refine the visual design of the dials (e.g., color gradients, labels).
- Explore advanced visualization libraries like Plotly or Dash for a web-based alternative.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI components.
- [Psutil](https://github.com/giampaolo/psutil) for system monitoring utilities.
- [Speedtest-cli](https://github.com/sivel/speedtest-cli) for network speed testing.
