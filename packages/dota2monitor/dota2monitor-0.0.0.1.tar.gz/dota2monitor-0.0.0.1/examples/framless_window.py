from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QFont
from flask import Flask, request
# import requests
import threading
from dota2monitor.server import Dota2Monitor
from dota2monitor.models import ListeningEvents

app = Flask(__name__)

# Updated notification functions with access to notify_label
def custom_lvl_up_notify():
    if notify_label:
        notify_label.setText('New level!')

def custom_death_notify():
    if notify_label:
        notify_label.setText('Dead!')

def custom_smoked_notify():
    if notify_label:
        notify_label.setText('Smoked!')

# Create global variable for label
notify_label = None

class NotificationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.oldPos = self.pos()  # Store the initial position

    def init_ui(self):
        layout = QVBoxLayout()

        self.notify_label = QLabel('Notifications will appear here.')
        self.notify_label.setFont(QFont('Arial', 20)) 
        self.notify_label.setStyleSheet("color: red;")  # Set text color to red
        layout.addWidget(self.notify_label)

        #communication with server example
        # button = QPushButton('Send Request')
        # button.clicked.connect(send_request)
        # layout.addWidget(button)

        self.setWindowTitle('Dota Monitor')
        self.setLayout(layout)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  # Set window frameless and always on top
        self.show()
        
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()  # Get the current position when the mouse is pressed

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()  # Update the old position for the next movement

# Create a function to send requests to Flask server
# def send_request():
#     response = requests.post('http://127.0.0.1:666/')  # Replace with your server address
#     # Process the response here if needed
#     print(response.text)

def run_server():
    monitor = Dota2Monitor()
    monitor.event_manager.add_event_listener("onDeath", custom_death_notify)
    monitor.event_manager.add_event_listener(ListeningEvents.LVL_UP, custom_lvl_up_notify)
    monitor.event_manager.add_event_listener(ListeningEvents.SMOKED, custom_smoked_notify)

    monitor.run(port = 666)

if __name__ == '__main__':

    flask_thread = threading.Thread(target=run_server)
    flask_thread.start()

    # Create QApplication instance
    app = QApplication([])

    # Create and show the notification window
    notify_window = NotificationWindow()
    notify_label = notify_window.notify_label  # Assign notify_label to the global variable

    app.exec_()
