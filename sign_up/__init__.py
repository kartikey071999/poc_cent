import logging
import json
from datetime import date
from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container  

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    container_name = 'users'
    container = get_db_container(container_name)

    try:
        req_body = req.get_json()
    except ValueError:
        return HttpResponse("Invalid JSON data in the request body.", status_code=400)
   
    obtained_patient_key = "12345" 
    user_id = "123" #mdflow ?
    
    
    user_data = {
        "id": user_id,
        "patient_id": obtained_patient_key, 
        "email": req_body.get('email', ''),
        "emergency_contact": req_body.get('em_name', '')  + req_body.get('em_relationship', '') +req_body.get('mobile_number', ''),
        "address" : req_body.get('line1') + req_body.get('line2') + req_body.get('city') + req_body.get('state') + req_body.get('zip_code'),
        "preferred_language" : req_body.get('preferred_language'),
        "preferred_communication" : req_body.get('preferred_communication'),
        "created_date" : date.today(),
    }

    container.create_item(body=user_data)
    logging.info("User account created successfully.")

    return HttpResponse("Account created successfully.", status_code=201)
