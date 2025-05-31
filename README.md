# Device Monitor

A cross-platform desktop application that allows you to monitor USB devices and network adapters connected to your computer in real-time.

![Screenshot of Device Monitor](https://via.placeholder.com/800x450.png?text=Device+Monitor+Screenshot)

## Features

- 🔍 Real-time detection of USB devices
- 🖧 Network adapter monitoring
- 🔄 Automatic refresh of device status
- 🌈 Modern, clean UI with dark theme
- 💻 Cross-platform (Windows, macOS, Linux)

## Installation

### Windows

1. Download the latest installer from the [Releases](https://github.com/YOUR_USERNAME/device-monitor/releases) page
2. Run the installer and follow the on-screen instructions
3. Launch Device Monitor from your Start Menu or desktop shortcut

### macOS & Linux

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python MyApp/main.py
   ```

## Building from Source

### Requirements

- Python 3.6 or higher
- PyQt5
- Additional requirements in `requirements.txt`

### Build Steps

1. Clone the repository:
   ```
   git clone https://github.com/ovalriver23/device-monitor.git
   cd device-monitor
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create executable:
   ```
   python build.py
   ```

4. For Windows, create installer (requires Inno Setup):
   ```
   python create_installer.py
   ```

## How It Works

Device Monitor uses platform-specific commands to detect and display information about connected devices:

- Windows: PowerShell commands
- macOS: system_profiler and networksetup
- Linux: lsusb and ip commands

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- PyQt5 for the UI framework
- All contributors who have helped to improve this project

---

Made with ❤️ by Tuana Melisa Aksoy
