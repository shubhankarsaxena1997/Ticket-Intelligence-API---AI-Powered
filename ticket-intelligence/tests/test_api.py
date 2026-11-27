from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_ticket(monkeypatch):
    def mock_graph_invoke(state):
        return {
            "language": "en",
            "is_english": True,
            "normalized_text": "Payment service is failing",
            "similar_tickets": [],
            "sla_analysis": {
                "sla_hours": 4,
                "elapsed_hours": 2,
                "remaining_hours": 2,
                "sla_breached": False
            },
            "final_analysis": "Payment service failure detected."
        }

    monkeypatch.setattr(
        "app.main.graph.invoke",
        mock_graph_invoke
    )

    ticket = {
        "ticket_id": "INC007",
        "short_description": "Payment service is failing",
        "priority": "P1",
        "status": "Open",
        "category": "Payment",
        "sla_hours": 4,
        "created_at": "2026-09-13T08:00:00",
        "resolved_at": None
    }

    response = client.post(
        "/tickets/analyze",
        json=ticket
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ticket_id"] == "INC007"
    assert data["language"] == "en"
    assert data["is_english"] is True
    assert data["normalized_text"] == "Payment service is failing"
    assert data["similar_tickets"] == []
    assert data["sla_analysis"]["sla_breached"] is False
    assert data["final_analysis"] == "Payment service failure detected."


def test_analyze_ticket_validation():
    invalid_ticket = {
        "ticket_id": "INC008",
        "short_description": "Payment service is failing"
    }

    response = client.post(
        "/tickets/analyze",
        json=invalid_ticket
    )

    assert response.status_code == 422
