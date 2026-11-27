from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import graph

app = FastAPI(
    title="Ticket Intelligence API",
    description="AI-powered Service Ticket Analyzer",
    version="1.0.0"
)


class TicketRequest(BaseModel):
    ticket_id: str
    short_description: str
    priority: str
    status: str
    category: str
    sla_hours: int
    created_at: str
    resolved_at: str | None = None


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Ticket Intelligence API is running"
    }


@app.post("/tickets/analyze")
def analyze_ticket(ticket: TicketRequest):
    result = graph.invoke({
        "ticket": ticket.model_dump()
    })

    return {
        "ticket_id": ticket.ticket_id,
        "language": result["language"],
        "is_english": result["is_english"],
        "normalized_text": result["normalized_text"],
        "similar_tickets": result["similar_tickets"],
        "sla_analysis": result["sla_analysis"],
        "final_analysis": result["final_analysis"]
    }