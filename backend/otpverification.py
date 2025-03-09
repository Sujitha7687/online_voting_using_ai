from twilio.rest import Client
from config import TWILIO_CONFIG
import mysql.connector
from config import DB_CONFIG
import random, datetime

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def send_otp(user_id, phone):
    """Generates and sends an OTP to the user's phone number."""
    otp = str(random.randint(100000, 999999))
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=5)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO otp (user_id, otp_code, expires_at) VALUES (%s, %s, %s)", 
                   (user_id, otp, expires_at))
    conn.commit()
    conn.close()

    client = Client(TWILIO_CONFIG["account_sid"], TWILIO_CONFIG["auth_token"])
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=TWILIO_CONFIG["phone_number"],
        to=phone
    )
    return message.sid

def verify_otp(user_id, otp):
    """Checks if the provided OTP is valid."""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT otp_code FROM otp WHERE user_id = %s AND expires_at > NOW()", (user_id,))
    record = cursor.fetchone()
    conn.close()

    return record and record["otp_code"] == otp
