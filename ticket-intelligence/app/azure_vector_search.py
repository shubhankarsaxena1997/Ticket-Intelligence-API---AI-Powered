import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from sentence_transformers import SentenceTransformer


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


def find_similar_tickets(query, top_k=3):

    query_embedding = model.encode(query).tolist()

    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=top_k,
        fields="description_vector"
    )

    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        select=[
            "ticket_id",
            "short_description",
            "description",
            "resolution",
            "resolution_notes"
        ],
        top=top_k
    )

    similar_tickets = []

    for result in results:
        similar_tickets.append({
            "ticket_id": result["ticket_id"],
            "short_description": result["short_description"],
            "description": result["description"],
            "resolution": result["resolution"],
            "resolution_notes": result["resolution_notes"],
            "score": result["@search.score"]
        })

    return similar_tickets


if __name__ == "__main__":

    query = "Customers are unable to complete payment transactions"

    results = find_similar_tickets(query, top_k=3)

    for result in results:
        print(
            result["ticket_id"],
            "|",
            round(result["score"], 3),
            "|",
            result["short_description"]
            if "short_description" in result
            else ""
        )