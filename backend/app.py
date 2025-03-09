from flask import Flask, request, jsonify
import mysql.connector
import random
import datetime

from config import DB_CONFIG

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# ✅ Step 1: Generate OTP (Stored in DB)
@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    data = request.json
    user_id = data.get("user_id")
    
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT phone FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        return jsonify({"error": "User not found"}), 400
    
    otp = str(random.randint(100000, 999999))
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=5)

    cursor.execute("INSERT INTO otp (user_id, otp_code, expires_at) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE otp_code=%s, expires_at=%s", 
                   (user_id, otp, expires_at, otp, expires_at))
    conn.commit()
    conn.close()

    return jsonify({"message": "OTP generated. Enter your phone number to verify.", "otp": otp}), 200  # OTP is returned for manual entry

# ✅ Step 2: Verify OTP Using Phone Number
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    user_id = data.get("user_id")
    otp = data.get("otp")
    phone = data.get("phone")

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT otp_code FROM otp WHERE user_id = %s AND expires_at > NOW()", (user_id,))
    record = cursor.fetchone()

    cursor.execute("SELECT phone FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not record or record["otp_code"] != otp:
        return jsonify({"error": "Invalid OTP"}), 400
    
    if user["phone"] != phone:
        return jsonify({"error": "Phone number mismatch"}), 400

    return jsonify({"message": "OTP verified successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
