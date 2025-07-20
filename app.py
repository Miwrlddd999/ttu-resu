from flask import Flask, request
from flask_cors import CORS
from database import db_connect
import logging
import requests

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

def send_sms(phone_number, message):
    url = "https://sms.arkesel.com/api/v2/send-sms"
    payload = {
        "sender": "TTU",
        "message": message,
        "recipients": [phone_number],
    }
    headers = {
        "api-key": "cEdMYkZJRmRqSm1JYVF6UG1Ib1I",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"SMS error: {e}")
        return False

WELCOME_MENU = (
    "CON Welcome to TTU Result Checker\n"
    "1. Check Results\n"
    "2. Exit"
)
ENTER_INDEX = "CON Enter your index number:"
THANK_YOU = "END Thank you for using TTU Result Checker."
INVALID_INPUT = "END Invalid input. Please try again."
NO_RECORD = "END No record found for the provided index number."
SMS_SENT = "END Your result has been sent via SMS."
SMS_FAILED = "END Failed to send SMS. Please try again later."

@app.route('/ussd', methods=['POST'])
def ussd():
    text = request.form.get('text', '')
    user_response = text.strip().split("*")
    response = ""

    try:
        if text == "":
            response = WELCOME_MENU

        elif user_response[0] == "1" and len(user_response) == 1:
            response = ENTER_INDEX

        elif user_response[0] == "1" and len(user_response) == 2:
            index = user_response[1]

            try:
                conn, cursor = db_connect()
                cursor.execute("SELECT name, grades, phone FROM students WHERE index_number = ?", (index,))
                record = cursor.fetchone()
                conn.close()
            except Exception as db_err:
                logging.error(f"Database error: {db_err}")
                return "END Internal server error.", 200, {'Content-Type': 'text/plain'}

            if record:
                name = record["name"]
                result = record["grades"]
                phone = record["phone"]
                message = f"Hi {name}, your result is: {result}"

                success = send_sms(phone, message)
                if success:
                    response = SMS_SENT
                else:
                    response = SMS_FAILED
            else:
                response = NO_RECORD

        elif user_response[0] == "2":
            response = THANK_YOU

        else:
            response = INVALID_INPUT

    except Exception as e:
        logging.error(f"USSD processing error: {e}")
        response = "END An unexpected error occurred. Please try again later."

    return response, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=True, port=5001)

       
