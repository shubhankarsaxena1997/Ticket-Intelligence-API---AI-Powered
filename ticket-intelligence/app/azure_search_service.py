import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
)

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
api_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

credential = AzureKeyCredential(api_key)

index_client = SearchIndexClient(
    endpoint=endpoint,
    credential=credential
)

fields = [
    SimpleField(
        name="ticket_id",
        type=SearchFieldDataType.String,
        key=True
    ),

    SearchableField(
        name="short_description",
        type=SearchFieldDataType.String
    ),

    SearchableField(
        name="description",
        type=SearchFieldDataType.String
    ),

    SearchableField(
        name="resolution",
        type=SearchFieldDataType.String
    ),

    SearchableField(
        name="resolution_notes",
        type=SearchFieldDataType.String
    ),

    SearchField(
        name="description_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=384,
        vector_search_profile_name="ticket-vector-profile"
    )
]

vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(
            name="ticket-hnsw"
        )
    ],
    profiles=[
        VectorSearchProfile(
            name="ticket-vector-profile",
            algorithm_configuration_name="ticket-hnsw"
        )
    ]
)

index = SearchIndex(
    name=index_name,
    fields=fields,
    vector_search=vector_search
)

result = index_client.create_or_update_index(index)

print(f"Index created: {result.name}")