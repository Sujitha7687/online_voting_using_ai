from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, QInputDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import requests

class VoteWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.user_id = None
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #333; color: white;")

        title = QLabel("Vote for Your Candidate")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.candidate1 = QPushButton("Candidate A")
        self.candidate1.setFont(QFont("Arial", 14))
        self.candidate1.setStyleSheet("background-color: #28a745; color: white; padding: 10px; border-radius: 5px;")
        self.candidate1.clicked.connect(lambda: self.request_otp("Candidate A"))

        self.candidate2 = QPushButton("Candidate B")
        self.candidate2.setFont(QFont("Arial", 14))
        self.candidate2.setStyleSheet("background-color: #dc3545; color: white; padding: 10px; border-radius: 5px;")
        self.candidate2.clicked.connect(lambda: self.request_otp("Candidate B"))

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.candidate1)
        layout.addWidget(self.candidate2)
        self.setLayout(layout)

    def request_otp(self, candidate):
        """Generates an OTP and verifies using the phone number."""
        response = requests.post("http://127.0.0.1:5000/generate_otp", json={"user_id": self.user_id})
        if response.status_code == 200:
            otp, ok1 = QInputDialog.getText(self, "OTP Verification", "Enter OTP:")
            phone, ok2 = QInputDialog.getText(self, "Phone Verification", "Enter your registered phone number:")

            if ok1 and ok2:
                verify_response = requests.post("http://127.0.0.1:5000/verify_otp", 
                    json={"user_id": self.user_id, "otp": otp, "phone": phone})
                
                if verify_response.status_code == 200:
                    self.cast_vote(candidate)
                else:
                    QMessageBox.warning(self, "Error", "OTP or phone verification failed!")
        else:
            QMessageBox.warning(self, "Error", "Failed to generate OTP!")

    def cast_vote(self, candidate):
        """Casts the vote after successful OTP and phone verification."""
        response = requests.post("http://127.0.0.1:5000/vote", json={"user_id": self.user_id, "candidate": candidate})
        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Vote cast successfully!")
        else:
            QMessageBox.warning(self, "Error", "Error casting vote!")
