import azure.functions as func
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    blob_url = req.params.get('blob_url')  # Extract the 'blob_url' parameter from the query string

    if blob_url is None:
        return func.HttpResponse("Blob URL parameter is missing in the query string.", status_code=400)

    try:
        # Send a GET request to the blob URL to retrieve the file
        response = requests.get(blob_url)

        if response.status_code == 200:
            # Extract the file content
            pdf_bytes = response.content
            print("PDF File")
            return func.HttpResponse(pdf_bytes, mimetype='application/pdf')
        else:
            print("Not Avilable : Error 404")
            return func.HttpResponse(f"Failed to retrieve the blob: {response.status_code}", status_code=response.status_code)
    except Exception as e:
        print("Error")
        return func.HttpResponse(f"Failed to retrieve the blob: {str(e)}", status_code=500)
