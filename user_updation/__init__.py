import logging

from azure.functions import HttpRequest, HttpResponse
from get_db_object import get_db_container


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    container_name = 'users'
    container = get_db_container(container_name)
    name = req.params.get('name')
    input_json = {
        "id": "1003",
        "patient_id": "333",
        "Created_date": "",
        "first_name": "Nikhil",
        "middle_name": "",
        "last_name": "sharma",
        "insurance_carrier_name": "",
        "gender": "M",
        "member_id": "101",
        "dob": "10/09/1996",
        "home_zip_code": "110094",
        "last_visit_date": "09/08/2023",
        "email": "nikhil@nikhil.com",
        "old_password": "1234",
        "is_verified": "true",
        "verified_at": "",
        "MPIN": "123",
        "is_locked": "No",
        "is_tmp_password": "No",
        "last_login_date": "09/08/2023",
    }
    container.create_item(body=input_json)
    logging.info("User details updated!!!")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
