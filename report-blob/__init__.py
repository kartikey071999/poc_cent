import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient, ContainerClient
import base64



def main(req: func.HttpRequest) -> func.HttpResponse:
    
   
    try:
        req_body = req.get_json()
        
       
    except ValueError:
        return func.HttpResponse("Invalid input data.", status_code=400)
    
    result = upload_lab_report(req_body)
    return func.HttpResponse("File uoloaded success.", status_code=200)

def upload_lab_report(input_data):
    connection_string = "DefaultEndpointsProtocol=https;AccountName=mdflowreportstorage;AccountKey=AI5X9RBxL823c2h6JYRJooFX2/PtVz6KV05r8cs/T770lt2dJExUTlmJ9z4B+bGrsuwBduBoSVIE+ASti1EBRw==;EndpointSuffix=core.windows.net"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_name = "report"                     
    container_client = blob_service_client.get_container_client(container_name)
   
    
    blob_name = f"{input_data['document_id']}_lab_report.pdf"
    blob_client = container_client.get_blob_client(blob_name)
    
    pdf_data = base64.b64decode(input_data["lab_report"])
    
    blob_client.upload_blob(pdf_data, overwrite=True)
    
    input_data1 = {
    "document_id": "12347",
    "Patient_id": "101",
    "Report date": "2023-09-27",
    "lab_report": "base64_encoded_pdf_data"
    }

    #blob_name = upload_lab_report(input_data)
    print(f"Lab report uploaded as blob: {blob_name}")
    return blob_name
