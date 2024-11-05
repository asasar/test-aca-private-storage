import os
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient



queue_url = os.environ.get("AzureWebJobsStorage__queueServiceUri")
blob_url = os.environ.get("AzureWebJobsStorage__blobServiceUri")

queue_client = QueueServiceClient(account_url=queue_url, credential=DefaultAzureCredential()).get_queue_client("jobs")
blob_client = BlobServiceClient(account_url=blob_url, credential=DefaultAzureCredential()).get_container_client("files")

blob_client.get_container_properties()

queue_client.peek_messages(max_messages=1)
logging.info("Queue exists.")

