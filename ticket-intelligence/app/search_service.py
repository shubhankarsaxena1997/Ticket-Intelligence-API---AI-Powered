import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


load_dotenv()

model = SentenceTransformer(os.getenv("TRANSFORMER_MODEL"))


def create_embedding(text):
    return model.encode(text)


def build_ticket_index(tickets):
    ticket_texts = [
        f"""
        Issue: {ticket["short_description"]}
        Description: {ticket["description"]}
        Resolution: {ticket["resolution"]}
        Resolution Notes: {ticket["resolution_notes"]}
        """
        for ticket in tickets
    ]

    # embeddings = model.encode(ticket_texts)
    embeddings = create_embedding(ticket_texts)

    return embeddings


def format_similar_tickets(results):
    context = ""

    for result in results:
        context += f"""
            Ticket ID: {result["ticket_id"]}
            Description: {result["description"]}
            Similarity: {result["similarity"]:.2f}

            """
    return context


def find_similar_tickets(query, tickets, ticket_embeddings, top_k=3):
    query_embedding = create_embedding(query)

    similarities = cosine_similarity( query_embedding.reshape(1, -1), ticket_embeddings )[0]

    results = []

    for ticket, score in zip(tickets, similarities):
        results.append({
            "ticket_id": ticket["ticket_id"],
            "description": ticket["description"],
            "resolution": ticket["resolution"],
            "resolution_notes": ticket["resolution_notes"],
            "similarity": float(score)
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results[:top_k]