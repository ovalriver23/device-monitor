from PyQt5.QtWidgets import QApplication, QStackedWidget
from ui.welcome_page import WelcomePage
from ui.info_page import InfoPage
from ui.devices_page import DevicesPage

app = QApplication([])

# Global dark theme
app.setStyleSheet("""
    QWidget {
        background-color: #141217;
    }
""")

stack = QStackedWidget()

# Navigation functions (defined after page creation)
def go_to_devices():
    stack.setCurrentWidget(devices_page)

def go_to_info():
    stack.setCurrentWidget(info_page)

def go_back_to_welcome():
    stack.setCurrentWidget(welcome_page)

# Pages
welcome_page = WelcomePage(go_to_devices, go_to_info)
info_page = InfoPage(go_back_to_welcome, go_to_devices)
devices_page = DevicesPage(go_back_to_welcome)

stack.addWidget(welcome_page)
stack.addWidget(info_page)
stack.addWidget(devices_page)

stack.setCurrentWidget(welcome_page)
stack.setFixedSize(1000, 800)
stack.show()
app.exec_()
