import os
import sys
import subprocess
import shutil
import tempfile
import platform
from build import create_executable

def create_windows_installer():
    """Create a Windows installer using Inno Setup."""
    print("\nCreating Windows installer...")
    
    # Check if Inno Setup is installed (by checking registry)
    inno_found = False
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
            for i in range(1000):  # Arbitrary large number to traverse all keys
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                            if "Inno Setup" in display_name:
                                inno_found = True
                                break
                        except:
                            pass
                except OSError:
                    break
    except:
        pass
    
    if not inno_found:
        print("Inno Setup not found. Please install Inno Setup from https://jrsoftware.org/isdl.php")
        return False
    
    # Create a temporary .iss script file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".iss", mode="w") as iss_file:
        app_version = "1.0.0"  # Set your version
        app_name = "Device Monitor"
        company_name = "Your Company"  # Replace with your company name
        
        # Get path to the executable
        exe_path = os.path.join(os.getcwd(), "dist", "DeviceMonitor.exe")
        if not os.path.exists(exe_path):
            print(f"Error: Executable not found at {exe_path}")
            return False
        
        # Create installer script content
        iss_content = f"""
[Setup]
AppName={app_name}
AppVersion={app_version}
AppPublisher={company_name}
DefaultDirName={{autopf}}\\{app_name}
DefaultGroupName={app_name}
UninstallDisplayIcon={{app}}\\DeviceMonitor.exe
Compression=lzma
SolidCompression=yes
OutputDir=installer
OutputBaseFilename=DeviceMonitor-Setup

[Files]
Source="{exe_path}"; DestDir="{{app}}"
Source="README.md"; DestDir="{{app}}"

[Icons]
Name="{{group}}\\{app_name}"; Filename="{{app}}\\DeviceMonitor.exe"
Name="{{commondesktop}}\\{app_name}"; Filename="{{app}}\\DeviceMonitor.exe"

[Run]
Filename="{{app}}\\DeviceMonitor.exe"; Description="Launch {app_name}"; Flags=postinstall nowait
"""
        
        iss_file.write(iss_content)
        iss_path = iss_file.name
    
    # Create installer output directory
    installer_dir = os.path.join(os.getcwd(), "installer")
    if not os.path.exists(installer_dir):
        os.makedirs(installer_dir)
    
    # Try to locate Inno Setup compiler
    inno_compiler_paths = [
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
    ]
    
    inno_compiler = None
    for path in inno_compiler_paths:
        if os.path.exists(path):
            inno_compiler = path
            break
    
    if not inno_compiler:
        print("Error: Could not find Inno Setup compiler (ISCC.exe)")
        return False
    
    # Run Inno Setup compiler
    print(f"Using Inno Setup compiler at: {inno_compiler}")
    print(f"Building installer from script: {iss_path}")
    
    result = subprocess.run([inno_compiler, iss_path])
    
    # Clean up temporary file
    os.unlink(iss_path)
    
    if result.returncode == 0:
        installer_path = os.path.join(installer_dir, "DeviceMonitor-Setup.exe")
        print(f"\nInstaller created successfully at: {installer_path}")
        return True
    else:
        print("\nInstaller creation failed!")
        return False

def create_deployment():
    """Create deployment package based on current platform."""
    if platform.system() != "Windows":
        print("Installer creation is currently only supported on Windows.")
        print("Only creating executable...")
        create_executable()
        return
    
    # Create the executable first
    create_executable()
    
    # Create installer
    create_windows_installer()

if __name__ == "__main__":
    create_deployment() 