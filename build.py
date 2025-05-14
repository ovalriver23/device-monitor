import os
import subprocess
import shutil
import sys

def create_executable():
    """Create a standalone executable using PyInstaller."""
    print("Starting build process...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Clean previous builds if they exist
    if os.path.exists("build"):
        print("Removing previous build directory...")
        shutil.rmtree("build")
    if os.path.exists("dist"):
        print("Removing previous dist directory...")
        shutil.rmtree("dist")
    
    # Create an icon file if it doesn't exist
    icon_path = os.path.join(os.getcwd(), "app_icon.ico")
    if not os.path.exists(icon_path):
        print("No icon file found. Skipping icon...")
        icon_param = []
    else:
        print(f"Using icon at {icon_path}")
        icon_param = ["--icon", icon_path]
    
    # Build command
    main_path = os.path.join(os.getcwd(), "MyApp", "main.py")
    command = [
        "pyinstaller",
        "--name=DeviceMonitor",
        "--onefile",
        "--windowed",
        *icon_param,
        "--clean",
        "--add-data", f"MyApp/ui{os.pathsep}ui",
        "--add-data", f"MyApp/core{os.pathsep}core",
        main_path
    ]
    
    # Run PyInstaller
    print("Running PyInstaller...")
    result = subprocess.run(command)
    
    if result.returncode == 0:
        print("\nBuild completed successfully!")
        exe_path = os.path.join(os.getcwd(), "dist", "DeviceMonitor.exe" if sys.platform == "win32" else "DeviceMonitor")
        print(f"Executable created at: {exe_path}")
    else:
        print("\nBuild failed!")

if __name__ == "__main__":
    create_executable() 