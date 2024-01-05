from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

app = Flask(__name__)

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r"protege-410212-48d137940bc9.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open_by_key("1MEU6t9DraDZSltYGPVlxmyyJKWsk1kQ8").Sheet1

def update_sheet(data, sheet):
    sheet.append_row(data)

def process_message(msg_body, sender):
    # Process your logic here
    # For example, extract data from the message and update the Google Sheet
    data_to_update = [sender, msg_body]
    update_sheet(data_to_update, sheet)

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body").lower()
    sender = request.form.get("From")

    response = MessagingResponse()
    message = response.message()

    if "hello" in incoming_msg:
        reply = "Hello! Please send your message to update the Google Sheet."
        message.body(reply)
    else:
        process_message(incoming_msg, sender)
        reply = "Your message has been processed and the Google Sheet updated."
        message.body(reply)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
