from flask import Flask, request, jsonify
import mysql.connector
import random
import datetime
from twilio.rest import Client
from config import DB_CONFIG, TWILIO_CONFIG

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# ✅ Step 1: Send OTP before voting
@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    user_id = data.get("user_id")
    
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT phone FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 400

    otp = str(random.randint(100000, 999999))
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=5)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO otp (user_id, otp_code, expires_at) VALUES (%s, %s, %s)", 
                   (user_id, otp, expires_at))
    conn.commit()
    conn.close()

    client = Client(TWILIO_CONFIG["account_sid"], TWILIO_CONFIG["auth_token"])
    client.messages.create(
        body=f"Your OTP for voting is {otp}",
        from_=TWILIO_CONFIG["phone_number"],
        to=user["phone"]
    )

    return jsonify({"message": "OTP sent successfully"}), 200

# ✅ Step 2: Verify OTP and cast vote
@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    user_id = data.get("user_id")
    otp = data.get("otp")
    candidate = data.get("candidate")

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT otp_code FROM otp WHERE user_id = %s AND expires_at > NOW()", (user_id,))
    record = cursor.fetchone()

    if not record or record["otp_code"] != otp:
        return jsonify({"error": "Invalid OTP"}), 400

    # Record vote in blockchain (logic not shown)
    # Store vote in MySQL
    cursor.execute("INSERT INTO votes (user_id, candidate) VALUES (%s, %s)", (user_id, candidate))
    conn.commit()
    conn.close()

    return jsonify({"message": "Vote cast successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
