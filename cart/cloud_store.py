from azure.cosmosdb.table import TableService
from dotenv import load_dotenv

load_dotenv()

# Database Connection
connection_string = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
if not connection_string:
    account_key = os.getenv("AZURE_COSMOS_ACCOUNT_KEY")
    account_name = os.getenv("AZURE_COSMOS_ACCOUNT_NAME")
    table_endpoint = os.getenv("AZURE_COSMOS_TABLE_ENDPOINT")
    connection_string = (
        f"DefaultEndpointsProtocol=https;"
        f"AccountName={account_name};"
        f"AccountKey={account_key};"
        f"TableEndpoint={table_endpoint};"
    )
TableService(
    endpoint_suffix="table.cosmos.azure.com", connection_string=connection_string
)
