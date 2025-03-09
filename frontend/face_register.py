from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import requests
import face_auth

class FaceRegisterWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #444; color: white;")
        
        title = QLabel("Register Face")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setFont(QFont("Arial", 14))
        self.name_input.setStyleSheet("padding: 10px; border-radius: 5px;")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        self.phone_input.setFont(QFont("Arial", 14))
        self.phone_input.setStyleSheet("padding: 10px; border-radius: 5px;")

        register_button = QPushButton("Capture Face & Register")
        register_button.setFont(QFont("Arial", 14))
        register_button.setStyleSheet("background-color: #17a2b8; color: white; padding: 10px; border-radius: 5px;")
        register_button.clicked.connect(self.register_face)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(register_button)
        self.setLayout(layout)

    def register_face(self):
        face_encoding = face_auth.register_face()
        name = self.name_input.text()
        phone = self.phone_input.text()

        if face_encoding and name and phone:
            requests.post("http://127.0.0.1:5000/register", json={"name": name, "phone": phone, "face_encoding": face_encoding})
            QMessageBox.information(self, "Success", "Face registered successfully!")
        else:
            QMessageBox.warning(self, "Error", "Registration failed!")
