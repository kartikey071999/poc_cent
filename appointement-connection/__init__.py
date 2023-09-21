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

    connection_string = "endpoint=https://con.unitedstates.communication.azure.com/;accesskey=e7HF+eTIl/UsHGjlw0OXB9slfNB8cYEFXXkwxWzk6axkhiAdbFR9ejRC5EqZ1Kpjmc7r47uPcTT4Gz2aZth0wQ=="
    client = EmailClient.from_connection_string(connection_string)

    message = {"senderAddress": "DoNotReply@623bac90-fff5-4997-8774-1adc57d02be8.azurecomm.net",
               "recipients": {
                   "to": [{"address": "kartikey071999@gmail.com"}],
               },
               "content": {
                   "subject": "Test Email",
                   "plainText": "Hello world via email.",
               }
               }

    poller = client.begin_send(message)
    result = poller.result()

    return func.HttpResponse(f"Email sent successfully to {email}")
