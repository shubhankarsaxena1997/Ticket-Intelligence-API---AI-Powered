from app.sla_analyzer import analyze_sla


def test_ticket_within_sla():
    ticket = {
        "ticket_id": "INC001",
        "sla_hours": 4,
        "created_at": "2026-09-13T08:00:00",
        "resolved_at": "2026-09-13T10:00:00"
    }

    result = analyze_sla(ticket)

    assert result["elapsed_hours"] == 2
    assert result["sla_breached"] is False
    assert result["remaining_hours"] == 2


def test_ticket_sla_breached():
    ticket = {
        "ticket_id": "INC002",
        "sla_hours": 4,
        "created_at": "2026-09-13T08:00:00",
        "resolved_at": "2026-09-13T13:00:00"
    }

    result = analyze_sla(ticket)

    assert result["elapsed_hours"] == 5
    assert result["sla_breached"] is True
    assert result["remaining_hours"] == 0


def test_ticket_exactly_at_sla_limit():
    ticket = {
        "ticket_id": "INC003",
        "sla_hours": 4,
        "created_at": "2026-09-13T08:00:00",
        "resolved_at": "2026-09-13T12:00:00"
    }

    result = analyze_sla(ticket)

    assert result["elapsed_hours"] == 4
    assert result["sla_breached"] is False
    assert result["remaining_hours"] == 0
    
    
def test_open_ticket_sla():
    ticket = {
        "ticket_id": "INC004",
        "sla_hours": 4,
        "created_at": "2026-09-13T08:00:00",
        "resolved_at": None
    }

    result = analyze_sla(ticket)

    assert result["ticket_id"] == "INC004"
    assert result["elapsed_hours"] >= 0
    assert result["remaining_hours"] >= 0
    assert isinstance(result["sla_breached"], bool)