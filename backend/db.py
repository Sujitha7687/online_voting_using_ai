import face_recognition
import cv2
import numpy as np
import mysql.connector
from config import DB_CONFIG

def register_face(user_id):
    """Captures a user's face and stores its encoding in the database."""
    video_capture = cv2.VideoCapture(0)
    print("Please align your face in the camera...")

    while True:
        _, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            encoding_str = ",".join(map(str, face_encodings))

            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET face_encoding = %s WHERE id = %s", (encoding_str, user_id))
            conn.commit()
            conn.close()
            print("Face registered successfully!")
            break

    video_capture.release()
    cv2.destroyAllWindows()

def verify_face():
    """Verifies if a face matches a registered user."""
    video_capture = cv2.VideoCapture(0)
    print("Scanning your face for login...")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, face_encoding FROM users WHERE face_encoding IS NOT NULL")
    users = cursor.fetchall()
    conn.close()

    known_encodings = {user["id"]: np.array(list(map(float, user["face_encoding"].split(",")))) for user in users}

    while True:
        _, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for encoding in face_encodings:
                matches = face_recognition.compare_faces(list(known_encodings.values()), encoding)
                if True in matches:
                    matched_id = list(known_encodings.keys())[matches.index(True)]
                    print(f"Face Verified! User ID: {matched_id}")
                    return matched_id  # Return the verified user ID

    video_capture.release()
    cv2.destroyAllWindows()
    return None
