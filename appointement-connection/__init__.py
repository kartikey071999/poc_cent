import logging

import azure.functions as func

from json import JSONDecodeError, JSONDecoder, JSONEncoder
from azure.communication.email import EmailClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if req.method == "POST":
        data = req.get_json()
        email = data.get('email')
        patient_id = data.get('patient_id')
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')

        if not email or not patient_id or not appointment_date or not appointment_time:
            return func.HttpResponse("Missing required data.", status_code=400)

        email_subject = "Appointment Confirmation"
        email_body = f"Hello,\n\nYour appointment has been confirmed. Here are the details:\n\n" \
                     f"Patient ID: {patient_id}\n" \
                     f"Appointment Date: {appointment_date}\n" \
                     f"Appointment Time: {appointment_time}\n\n" \
                     f"Thank you for choosing our service!\n\nBest regards!"
        
        
        
    connection_string = "endpoint=https://con.unitedstates.communication.azure.com/;accesskey=e7HF+eTIl/UsHGjlw0OXB9slfNB8cYEFXXkwxWzk6axkhiAdbFR9ejRC5EqZ1Kpjmc7r47uPcTT4Gz2aZth0wQ=="
    client = EmailClient.from_connection_string(connection_string)

    message = {"senderAddress": "DoNotReply@623bac90-fff5-4997-8774-1adc57d02be8.azurecomm.net",
               "recipients": {
                   "to": [{"address": email}],
               },
               "content": {
                    "subject": email_subject,
                    "plainText": email_body,
                    "html": f"<html><p>{email_body}</p></html>"
               }
               }

    poller = client.begin_send(message)
    result = poller.result()

    return func.HttpResponse(f"Email sent successfully to {email}")
