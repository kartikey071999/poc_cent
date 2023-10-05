import azure.functions as func
import json
from azure.cosmos import CosmosClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    cosmosdb_endpoint = "https://centdb-poc.documents.azure.com:443/"
    cosmosdb_key = "meRQiMHhjAKuWnqTaGFA6bqTGeRmM0gJ5CNAPSyOVxmXxOBrVR4jHbzfXeqyDE6jV9MdlSNrg8saACDblt529g=="
    database_name = "centdb"
    container_name = "doc_id"

    from_date = req.params.get('from_date')
    to_date = req.params.get('to_date')
    center_id = req.params.get('center_id')
    patient_id = req.params.get('patient_id')

    client = CosmosClient(cosmosdb_endpoint, cosmosdb_key)

    database = client.get_database_client(database_name)

    container = database.get_container_client(container_name)

    query = f"""
        SELECT c.id, c.report_date
        FROM items as c
        WHERE c.center_id = '{center_id}'  
        AND c.patient_id = '{patient_id}'  
        AND CONVERT(DATE, c.report_date, 101) BETWEEN CONVERT(DATE, '{from_date}', 101) AND CONVERT(DATE, '{to_date}', 101);

    """
    items = list(container.query_items(query, enable_cross_partition_query=True))
    print(items)

    # Extract and transform the data while comparing the dates
    result = []
    for item in items:
        record = {
            "document_id": item['id'],
            "report_date": item['report_date']
        }
        print(item['id'])
        if compare_dates(record["report_date"], from_date) >= 0 and compare_dates(record["report_date"], to_date) <= 0:
            result.append(record)

    # Return the filtered data as JSON
    return func.HttpResponse(json.dumps(result), mimetype="application/json")

def compare_dates(date1, date2):
    parts1 = date1.split('/')
    parts2 = date2.split('/')
    
    year1, month1, day1 = int(parts1[2]), int(parts1[0]), int(parts1[1])
    year2, month2, day2 = int(parts2[2]), int(parts2[0]), int(parts2[1])
    
    if year1 > year2:
        return 1
    elif year1 < year2:
        return -1
    elif month1 > month2:
        return 1
    elif month1 < month2:
        return -1
    elif day1 > day2:
        return 1
    elif day1 < day2:
        return -1
    else:
        return 0
