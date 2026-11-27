from app.graph import graph


def test_graph_with_english_ticket(monkeypatch):

    def mock_search(query, tickets, embeddings, top_k=3):
        return [
            {
                "ticket_id": "INC005",
                "description": "Payment service unavailable",
                "resolution": "Database connection pool was adjusted.",
                "resolution_notes": "Database connections were exhausted.",
                "similarity": 0.85
            }
        ]

    def mock_analysis(ticket, similar_tickets, sla_analysis):
        return "Mocked final analysis"

    monkeypatch.setattr(
        "app.graph.find_similar_tickets",
        mock_search
    )

    monkeypatch.setattr(
        "app.graph.analyze_with_history",
        mock_analysis
    )

    ticket = {
        "ticket_id": "TEST001",
        "short_description": "Payment service is failing",
        "priority": "P1",
        "status": "Open",
        "category": "Payment",
        "sla_hours": 4,
        "created_at": "2026-09-13T08:00:00",
        "resolved_at": "2026-09-13T10:00:00"
    }

    result = graph.invoke({"ticket": ticket})

    assert result["language"] == "en"
    assert result["is_english"] is True
    assert result["normalized_text"] == "Payment service is failing"

    assert len(result["similar_tickets"]) == 1
    assert result["similar_tickets"][0]["ticket_id"] == "INC005"

    assert result["sla_analysis"]["sla_breached"] is False
    assert result["final_analysis"] == "Mocked final analysis"
    
    
def test_graph_with_non_english_ticket(monkeypatch):

    def mock_translate(ticket, language):
        return "Payment service is failing"

    def mock_search(query, tickets, embeddings, top_k=3):
        return []

    def mock_analysis(ticket, similar_tickets, sla_analysis):
        return "Mocked translated ticket analysis"

    monkeypatch.setattr(
        "app.graph.normalize_ticket_language",
        mock_translate
    )

    monkeypatch.setattr(
        "app.graph.find_similar_tickets",
        mock_search
    )

    monkeypatch.setattr(
        "app.graph.analyze_with_history",
        mock_analysis
    )

    ticket = {
        "ticket_id": "TEST002",
        "short_description": "El servicio de pago no está disponible",
        "priority": "P1",
        "status": "Open",
        "category": "Payment",
        "sla_hours": 4,
        "created_at": "2026-09-13T08:00:00",
        "resolved_at": "2026-09-13T10:00:00"
    }

    result = graph.invoke({"ticket": ticket})

    assert result["language"] == "es"
    assert result["is_english"] is False
    assert result["normalized_text"] == "Payment service is failing"
    assert result["final_analysis"] == "Mocked translated ticket analysis"