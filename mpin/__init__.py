import azure.functions as func
import json
from azure.cosmos import CosmosClient

# add it later according to exl
cosmos_connection_string = ""
container_name = ""

def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method != "POST":
        return func.HttpResponse("Method is not Post", status_code=405)

    try:
        req_body = req.get_json()
        member_id = req_body.get("member_id")
        mpin = req_body.get("mpin")

        if not member_id or not mpin:
            return func.HttpResponse("member_id and mpin are required in the input JSON", status_code=400)

        client = CosmosClient.from_connection_string(cosmos_connection_string)
        database = client.get_database_client("YOUR_DATABASE_NAME")
        container = database.get_container_client(container_name)

        response = container.read_item(item=member_id, partition_key=member_id)

        current_mpin = response["current_mpin"]
        last_mpin = response["last_mpin"]
        last_mpin2 = response["last_mpin2"]
        if mpin == current_mpin or mpin == last_mpin or mpin == last_mpin2:
            return func.HttpResponse("Input mpin matches one of the existing mpin values", status_code=200)

        response["last_mpin2"] = last_mpin
        response["last_mpin"] = current_mpin
        response["current_mpin"] = mpin

        container.upsert_item(body=response)
        
        return func.HttpResponse("Data updated successfully", status_code=200)

    except ValueError:
        return func.HttpResponse("Invalid JSON format", status_code=400)
