from azure.cosmos import CosmosClient

COSMOS_ENDPOINT = "https://centdb-poc.documents.azure.com:443/"
COSMOS_KEY = "meRQiMHhjAKuWnqTaGFA6bqTGeRmM0gJ5CNAPSyOVxmXxOBrVR4jHbzfXeqyDE6jV9MdlSNrg8saACDblt529g=="
DATABASE_NAME = "centdb"


def get_db_container(container_name):
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(container_name)
    return container
