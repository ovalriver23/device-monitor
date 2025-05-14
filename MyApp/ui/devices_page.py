from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QScrollArea, QFrame, QGridLayout, QSplitter)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont
from ui.styles import APP_STYLE
from core.device_scanner import DeviceScanner

class DeviceCard(QFrame):
    """Card widget to display device information."""
    
    def __init__(self, device_info):
        super().__init__()
        self.device_info = device_info
        self.init_ui()
        
    def init_ui(self):
        self.setObjectName("deviceCard")
        self.setStyleSheet("""
            QFrame#deviceCard {
                background-color: #1E1E1E;
                border-radius: 8px;
                padding: 12px;
                margin: 5px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QLabel#deviceName {
                font-size: 18px;
                font-weight: bold;
                color: #FFFFFF;
            }
            QLabel#deviceType {
                font-size: 14px;
                color: #9388A2;
            }
            QLabel#deviceDetail {
                font-size: 14px;
                color: #E5E8EB;
            }
            QLabel#deviceStatus {
                font-size: 14px;
                color: #66DD91;
                font-weight: bold;
            }
            QLabel#deviceDisconnected {
                font-size: 14px;
                color: #F87272;
                font-weight: bold;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # Device name
        name_label = QLabel(self.device_info.get('name', 'Unknown Device'))
        name_label.setObjectName("deviceName")
        layout.addWidget(name_label, 0, 0, 1, 2)
        
        # Device type
        type_label = QLabel(self.device_info.get('type', 'Unknown Type'))
        type_label.setObjectName("deviceType")
        layout.addWidget(type_label, 1, 0)
        
        # Status
        connected = self.device_info.get('connected', False)
        status_label = QLabel("Connected" if connected else "Disconnected")
        status_label.setObjectName("deviceStatus" if connected else "deviceDisconnected")
        layout.addWidget(status_label, 1, 1, alignment=Qt.AlignRight)
        
        # Additional details
        row = 2
        for key, value in self.device_info.items():
            # Skip the keys we've already displayed or internal keys
            if key in ['name', 'type', 'connected'] or key.startswith('_'):
                continue
                
            if value:
                detail_label = QLabel(f"{key.replace('_', ' ').title()}: {value}")
                detail_label.setObjectName("deviceDetail")
                layout.addWidget(detail_label, row, 0, 1, 2)
                row += 1
        
        self.setLayout(layout)


class DevicesPage(QWidget):
    """Page displaying all detected devices."""
    
    def __init__(self, go_back_callback):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.device_scanner = DeviceScanner()
        
        self.setStyleSheet("""
            QWidget {
                background-color: #141217;
                color: #FFFFFF;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            QPushButton {
                background-color: #801AE5;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 16px 24px;
                font-weight: bold;
                font-size: 20px;
                min-width: 160px;
                max-width: 250px;
                height: 35px;
            }
            QPushButton:hover {
                background-color: #9025F5;
                min-width: 170px;
                height: 40px;
                font-size: 21px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background-color: #7015D5;
                min-width: 165px;
                height: 38px;
            }
            QPushButton#secondary {
                background-color: #302938;
            }
            QPushButton#secondary:hover {
                background-color: #403948;
                min-width: 170px;
                height: 40px;
                font-size: 21px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            QPushButton#secondary:pressed {
                background-color: #201928;
                min-width: 165px;
                height: 38px;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #FFFFFF;
            }
            QLabel#sectionTitle {
                font-size: 20px;
                font-weight: bold;
                color: #FFFFFF;
                margin-top: 20px;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QSplitter::handle {
                background-color: #333333;
            }
        """)
        
        self.init_ui()
        
        # Set up a timer to refresh device list periodically
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_devices)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header with back button
        header_layout = QHBoxLayout()
        
        back_button = QPushButton("Go Back")
        back_button.setObjectName("secondary")
        back_button.clicked.connect(self.go_back_callback)
        
        title = QLabel("Connected Devices")
        title.setObjectName("title")
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_devices)
        
        header_layout.addWidget(back_button)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(refresh_button)
        
        main_layout.addLayout(header_layout)
        
        # Create a splitter to allow resizing sections
        splitter = QSplitter(Qt.Vertical)
        
        # USB Devices Section
        usb_section = QWidget()
        usb_layout = QVBoxLayout(usb_section)
        usb_layout.setContentsMargins(0, 0, 0, 0)
        
        usb_title = QLabel("USB Devices")
        usb_title.setObjectName("sectionTitle")
        usb_layout.addWidget(usb_title)
        
        self.usb_devices_area = QScrollArea()
        self.usb_devices_area.setWidgetResizable(True)
        self.usb_devices_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.usb_devices_container = QWidget()
        self.usb_devices_layout = QVBoxLayout(self.usb_devices_container)
        self.usb_devices_layout.setAlignment(Qt.AlignTop)
        self.usb_devices_area.setWidget(self.usb_devices_container)
        
        usb_layout.addWidget(self.usb_devices_area)
        splitter.addWidget(usb_section)
        
        # Network Adapters Section
        network_section = QWidget()
        network_layout = QVBoxLayout(network_section)
        network_layout.setContentsMargins(0, 0, 0, 0)
        
        network_title = QLabel("Network Adapters")
        network_title.setObjectName("sectionTitle")
        network_layout.addWidget(network_title)
        
        self.network_devices_area = QScrollArea()
        self.network_devices_area.setWidgetResizable(True)
        self.network_devices_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.network_devices_container = QWidget()
        self.network_devices_layout = QVBoxLayout(self.network_devices_container)
        self.network_devices_layout.setAlignment(Qt.AlignTop)
        self.network_devices_area.setWidget(self.network_devices_container)
        
        network_layout.addWidget(self.network_devices_area)
        splitter.addWidget(network_section)
        
        main_layout.addWidget(splitter)
        
        self.setLayout(main_layout)
        
        # Initial device scan
        self.refresh_devices()
    
    def refresh_devices(self):
        """Refresh the device list."""
        # Clear current devices
        self._clear_layout(self.usb_devices_layout)
        self._clear_layout(self.network_devices_layout)
        
        # Get connected devices
        devices = self.device_scanner.get_connected_devices()
        network_adapters = self.device_scanner.get_network_adapters()
        
        # Add device cards to layout
        if devices:
            for device in devices:
                self.usb_devices_layout.addWidget(DeviceCard(device))
        else:
            no_devices_label = QLabel("No USB devices detected")
            no_devices_label.setAlignment(Qt.AlignCenter)
            self.usb_devices_layout.addWidget(no_devices_label)
        
        # Add network adapter cards to layout
        if network_adapters:
            for adapter in network_adapters:
                self.network_devices_layout.addWidget(DeviceCard(adapter))
        else:
            no_adapters_label = QLabel("No network adapters detected")
            no_adapters_label.setAlignment(Qt.AlignCenter)
            self.network_devices_layout.addWidget(no_adapters_label)
    
    def _clear_layout(self, layout):
        """Clear all widgets from a layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                
    def showEvent(self, event):
        """Overriden show event to refresh devices when page is shown."""
        super().showEvent(event)
        self.refresh_devices()
        
    def hideEvent(self, event):
        """Overriden hide event to stop timer when page is hidden."""
        super().hideEvent(event)
        self.refresh_timer.stop()
