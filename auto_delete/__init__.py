import pytz
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime, timedelta



def main(req: func.HttpRequest) -> func.HttpResponse:
        connection_string = "DefaultEndpointsProtocol=https;AccountName=mdflowreportstorage;AccountKey=AI5X9RBxL823c2h6JYRJooFX2/PtVz6KV05r8cs/T770lt2dJExUTlmJ9z4B+bGrsuwBduBoSVIE+ASti1EBRw==;EndpointSuffix=core.windows.net"

        container_name = "report" 

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(container_name)

        blob_names = []
        
        six_months_ago = datetime.now() - timedelta(days=180)
        six_months_ago = six_months_ago.replace(tzinfo=pytz.UTC)

        blob_list = container_client.list_blobs()

        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob)
            blob_properties = blob_client.get_blob_properties()
            last_modified = blob_properties['last_modified']

            if last_modified < six_months_ago:
                print(f"Deleting blob: {blob.name}")
                blob_names.append(blob.name)
                container_client.delete_blob(blob.name)
        
        response_body = json.dumps({"msg": "deleting files", "blob_names": blob_names})
        return func.HttpResponse(response_body,status_code=200, mimetype="application/json")

