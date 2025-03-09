# 🗳️ Online Voting System with Blockchain & Face Authentication

## 🚀 Project Description
A **secure online voting system** using:
- **Blockchain** for securing votes
- **Face Authentication** for voter verification
- **OTP Verification using the stored phone number**
- **MySQL for user and vote data**
- **Modern PyQt5 UI**

---

## 📁 Project Structure
online_voting_system/
│── backend/                # Flask Backend
│   ├── app.py              # Main Flask API
│   ├── blockchain.py       # Blockchain logic
│   ├── db.py               # MySQL connection
│   ├── face_auth.py        # Face recognition logic
│   ├── otp_verification.py # OTP authentication
│   ├── requirements.txt    # Dependencies
│
│── frontend/               # PyQt5 Frontend
│   ├── main.py             # UI logic
│   ├── login_ui.py         # Login page UI
│   ├── vote_ui.py          # Voting UI
│   ├── face_register.py    # Face registration
│
│── database/               # MySQL Database setup
│   ├── schema.sql          # Database schema
│
│── config.py               # Configuration (DB, Twilio, etc.)
│── README.md               # Documentation
