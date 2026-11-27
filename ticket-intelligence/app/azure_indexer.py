import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from sentence_transformers import SentenceTransformer

from ticket_service import load_tickets


load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
api_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

credential = AzureKeyCredential(api_key)

search_client = SearchClient(
    endpoint=endpoint,
    index_name=index_name,
    credential=credential
)

model = SentenceTransformer(os.getenv("TRANSFORMER_MODEL"))


tickets = load_tickets()

documents = []

for ticket in tickets:

    text = f"""
    Issue: {ticket["short_description"]}
    Description: {ticket["description"]}
    Resolution: {ticket["resolution"]}
    Resolution Notes: {ticket["resolution_notes"]}
    """

    embedding = model.encode(text).tolist()

    documents.append({
        "ticket_id": ticket["ticket_id"],
        "short_description": ticket["short_description"],
        "description": ticket["description"],
        "resolution": ticket["resolution"],
        "resolution_notes": ticket["resolution_notes"],
        "description_vector": embedding
    })
    
    

result = search_client.upload_documents(documents)

for item in result:
    print(
        f"{item.key}: "
        f"{'Success' if item.succeeded else 'Failed'}"
    )