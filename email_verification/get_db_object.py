from azure.cosmos import CosmosClient

COSMOS_ENDPOINT = "https://centdb.documents.azure.com:443/"
COSMOS_KEY = "4BRszznHrLpJ1MfRe1lnA5RQFVrxt8jwCoZobCDFNOQRdwn12ACa83xuI3nFbK2aysFpRcbTDq6OACDb6xIfdA=="
DATABASE_NAME = "cent"
CONTAINER_NAME = "email_data"


def get_db_container():
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
    return container
