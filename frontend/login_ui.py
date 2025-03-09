from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import face_auth
import requests

class LoginWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #222; color: white;")
        
        title = QLabel("Secure Voting Login")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        face_button = QPushButton("Login with Face Recognition")
        face_button.setFont(QFont("Arial", 14))
        face_button.setStyleSheet("background-color: #007bff; color: white; padding: 10px; border-radius: 5px;")
        face_button.clicked.connect(self.authenticate_user)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(face_button)
        self.setLayout(layout)

    def authenticate_user(self):
        user_id = face_auth.verify_face()
        if user_id:
            requests.post("http://127.0.0.1:5000/login", json={"face_encoding": user_id})
            self.parent.setCurrentWidget(self.parent.vote_screen)
