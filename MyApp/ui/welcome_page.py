from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from ui.styles import APP_STYLE

class WelcomePage(QWidget):
    def __init__(self, go_to_devices_callback, go_to_info_callback):
        super().__init__()
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
            QLabel {
                color: #FFFFFF;
            }
            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: #FFFFFF;
            }
            QLabel#welcome {
                font-size: 32px;
                font-weight: bold;
                color: #FFFFFF;
            }
            QLabel#subtitle {
                font-size: 22px;
                color: #E5E8EB;
                line-height: 1.6;
            }
        """)
        self.init_ui(go_to_devices_callback, go_to_info_callback)

    def init_ui(self, go_to_devices_callback, go_to_info_callback):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setSpacing(20)

        # Header
        header = QHBoxLayout()
        title = QLabel("Device Monitor")
        title.setObjectName("title")
        header.addWidget(title)
        header.addStretch()

        # Main content
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(40)
        
        welcome_title = QLabel("Welcome to Device Monitor")
        welcome_title.setObjectName("welcome")
        welcome_title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("See all your connected devices in one place. Monitor their status and activity, and manage them with ease.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setMinimumWidth(600)

        # Main buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        start_button = QPushButton("Start")
        start_button.clicked.connect(go_to_devices_callback)
        
        info_button = QPushButton("What this app does")
        info_button.setObjectName("secondary")
        info_button.clicked.connect(go_to_info_callback)

        button_layout.addWidget(start_button)
        button_layout.addWidget(info_button)

        content_layout.addWidget(welcome_title)
        content_layout.addWidget(subtitle)
        content_layout.addLayout(button_layout)

        # Add layouts with spacing
        main_layout.addLayout(header)
        main_layout.addStretch(1)
        main_layout.addLayout(content_layout)
        main_layout.addStretch(2)

        self.setLayout(main_layout)
        self.setMinimumSize(1000, 800)
