import os
import platform
import re
import subprocess
from typing import List, Dict, Any

class DeviceScanner:
    """Class to scan and retrieve information about connected devices."""
    
    def __init__(self):
        self.system = platform.system()
        
    def get_connected_devices(self) -> List[Dict[str, Any]]:
        """Get a list of all connected devices.
        
        Returns:
            List of dictionaries containing device information.
        """
        if self.system == "Windows":
            return self._get_windows_devices()
        elif self.system == "Darwin":  # macOS
            return self._get_macos_devices()
        elif self.system == "Linux":
            return self._get_linux_devices()
        else:
            return []
    
    def _get_windows_devices(self) -> List[Dict[str, Any]]:
        """Get connected devices on Windows using PowerShell."""
        devices = []
        
        try:
            # PowerShell command to get USB devices
            cmd = "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' } | Select-Object Status, Class, FriendlyName, InstanceId | ConvertTo-Json"
            result = subprocess.run(["powershell", "-Command", cmd], 
                                   capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                import json
                # PowerShell might return a single object or an array
                output = json.loads(result.stdout)
                
                # Ensure we have a list
                if isinstance(output, dict):
                    output = [output]
                
                for device in output:
                    devices.append({
                        'name': device.get('FriendlyName', 'Unknown Device'),
                        'type': device.get('Class', 'Unknown'),
                        'id': device.get('InstanceId', ''),
                        'status': device.get('Status', 'Unknown'),
                        'connected': device.get('Status') == 'OK'
                    })
        except Exception as e:
            print(f"Error scanning Windows devices: {e}")
        
        return devices
    
    def _get_macos_devices(self) -> List[Dict[str, Any]]:
        """Get connected devices on macOS using system_profiler."""
        devices = []
        
        try:
            result = subprocess.run(["system_profiler", "SPUSBDataType", "-json"], 
                                   capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                import json
                data = json.loads(result.stdout)
                
                # Parse the USB devices from the system_profiler output
                usb_items = data.get('SPUSBDataType', [])
                for usb_controller in usb_items:
                    self._parse_macos_usb_device(usb_controller, devices)
        except Exception as e:
            print(f"Error scanning macOS devices: {e}")
        
        return devices
    
    def _parse_macos_usb_device(self, device, devices_list, depth=0):
        """Recursively parse macOS USB device information."""
        if "_items" in device:
            for item in device["_items"]:
                self._parse_macos_usb_device(item, devices_list, depth+1)
        
        # Skip the root USB controllers
        if depth > 0 and "manufacturer" in device:
            devices_list.append({
                'name': device.get('_name', 'Unknown Device'),
                'type': 'USB',
                'id': device.get('location_id', ''),
                'manufacturer': device.get('manufacturer', 'Unknown'),
                'serial_number': device.get('serial_num', ''),
                'connected': True
            })
    
    def _get_linux_devices(self) -> List[Dict[str, Any]]:
        """Get connected devices on Linux using lsusb."""
        devices = []
        
        try:
            # Get device information using lsusb
            result = subprocess.run(["lsusb"], capture_output=True, text=True, check=True)
            
            # Parse lsusb output
            pattern = r'Bus (\d+) Device (\d+): ID (\w+):(\w+) (.*)'
            
            for line in result.stdout.strip().split('\n'):
                match = re.match(pattern, line)
                if match:
                    bus, device_num, vendor_id, product_id, description = match.groups()
                    
                    devices.append({
                        'name': description,
                        'type': 'USB',
                        'bus': bus,
                        'device': device_num,
                        'vendor_id': vendor_id,
                        'product_id': product_id,
                        'connected': True
                    })
        except Exception as e:
            print(f"Error scanning Linux devices: {e}")
        
        return devices
    
    def get_network_adapters(self) -> List[Dict[str, Any]]:
        """Get information about network adapters."""
        if self.system == "Windows":
            return self._get_windows_network()
        elif self.system == "Darwin":  # macOS
            return self._get_macos_network()
        elif self.system == "Linux":
            return self._get_linux_network()
        else:
            return []
    
    def _get_windows_network(self) -> List[Dict[str, Any]]:
        """Get network adapters on Windows."""
        adapters = []
        
        try:
            # PowerShell command to get network adapters
            cmd = "Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, MacAddress, LinkSpeed | ConvertTo-Json"
            result = subprocess.run(["powershell", "-Command", cmd], 
                                   capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                import json
                # PowerShell might return a single object or an array
                output = json.loads(result.stdout)
                
                # Ensure we have a list
                if isinstance(output, dict):
                    output = [output]
                
                for adapter in output:
                    adapters.append({
                        'name': adapter.get('Name', 'Unknown Adapter'),
                        'description': adapter.get('InterfaceDescription', ''),
                        'status': adapter.get('Status', 'Unknown'),
                        'mac_address': adapter.get('MacAddress', ''),
                        'speed': adapter.get('LinkSpeed', ''),
                        'connected': adapter.get('Status') == 'Up'
                    })
        except Exception as e:
            print(f"Error getting Windows network adapters: {e}")
        
        return adapters
    
    def _get_macos_network(self) -> List[Dict[str, Any]]:
        """Get network adapters on macOS."""
        adapters = []
        
        try:
            # Get network interfaces using networksetup
            result = subprocess.run(["networksetup", "-listallhardwareports"], 
                                   capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                current_adapter = {}
                
                for line in result.stdout.strip().split('\n'):
                    if line.startswith("Hardware Port:"):
                        # Start a new adapter
                        if current_adapter:
                            adapters.append(current_adapter)
                        current_adapter = {'name': line.split(": ")[1], 'connected': False}
                    elif line.startswith("Device:"):
                        current_adapter['device'] = line.split(": ")[1]
                    elif line.startswith("Ethernet Address:"):
                        current_adapter['mac_address'] = line.split(": ")[1]
                
                # Add the last adapter
                if current_adapter:
                    adapters.append(current_adapter)
                
                # Get status information for each adapter
                for adapter in adapters:
                    if 'device' in adapter:
                        result = subprocess.run(["ifconfig", adapter['device']], 
                                              capture_output=True, text=True, check=False)
                        adapter['connected'] = "status: active" in result.stdout.lower()
        except Exception as e:
            print(f"Error getting macOS network adapters: {e}")
        
        return adapters
    
    def _get_linux_network(self) -> List[Dict[str, Any]]:
        """Get network adapters on Linux."""
        adapters = []
        
        try:
            # Run ip addr to get network interfaces
            result = subprocess.run(["ip", "addr"], capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                current_device = None
                
                for line in result.stdout.strip().split('\n'):
                    if ': ' in line and not line.startswith(' '):
                        # New interface section
                        parts = line.split(': ')
                        current_device = {
                            'name': parts[1],
                            'connected': 'UP' in line,
                            'mac_address': ''
                        }
                        adapters.append(current_device)
                    elif current_device and 'link/ether' in line:
                        # MAC address line
                        mac = line.split()[1]
                        current_device['mac_address'] = mac
        except Exception as e:
            print(f"Error getting Linux network adapters: {e}")
        
        return adapters
