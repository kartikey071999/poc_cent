import azure.functions as func
from azure.cosmos import CosmosClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
        if data is not None:
            endpoint = "https://centlocation.documents.azure.com:443/"
            key = "HRFliLsotxSLYMZl2YqEb6gUUG4mKvux86iliJS2qVdpbxXwSrb6r1kRLTTFJDkVetjjJLzSlgpeACDbYhpn2g=="
            client = CosmosClient(endpoint, key)
            database_name = "centlocation"
            container_name = "Name"
            container = client.get_database_client(database_name).get_container_client(container_name)
            container.create_item(body=data)

            return func.HttpResponse("Data inserted successfully.", status_code=200)
        else:
            return func.HttpResponse("Invalid data provided.", status_code=400)
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
