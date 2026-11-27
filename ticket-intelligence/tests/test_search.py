from app.search_service import (
    build_ticket_index,
    find_similar_tickets
)


def test_build_ticket_index():
    tickets = [
        {
            "ticket_id": "INC001",
            "short_description": "Payment API returning 500 errors",
            "description": "Payment requests are failing.",
            "resolution": "Fixed payment validation service.",
            "resolution_notes": "Application exception was corrected."
        },
        {
            "ticket_id": "INC002",
            "short_description": "Payment transaction failures",
            "description": "Customers cannot complete payments.",
            "resolution": "Database connection pool was increased.",
            "resolution_notes": "Connection pool had reached its limit."
        }
    ]

    embeddings = build_ticket_index(tickets)

    assert embeddings is not None
    assert len(embeddings) == 2


def test_find_similar_tickets():
    tickets = [
        {
            "ticket_id": "INC001",
            "short_description": "Payment API returning 500 errors",
            "description": "Payment requests are failing.",
            "resolution": "Fixed payment validation service.",
            "resolution_notes": "Application exception was corrected."
        },
        {
            "ticket_id": "INC002",
            "short_description": "Payment transaction failures",
            "description": "Customers cannot complete payments.",
            "resolution": "Database connection pool was increased.",
            "resolution_notes": "Connection pool had reached its limit."
        },
        {
            "ticket_id": "INC003",
            "short_description": "Password reset not working",
            "description": "Users cannot reset their passwords.",
            "resolution": "Fixed email configuration.",
            "resolution_notes": "SMTP configuration was corrected."
        }
    ]

    embeddings = build_ticket_index(tickets)

    query = "Customers are unable to complete payment transactions"

    results = find_similar_tickets(
        query,
        tickets,
        embeddings,
        top_k=3
    )

    assert len(results) == 3
    assert results[0]["ticket_id"] in ["INC001", "INC002"]
    assert "similarity" in results[0]


def test_search_results_are_sorted():
    tickets = [
        {
            "ticket_id": "INC001",
            "short_description": "Payment API returning 500 errors",
            "description": "Payment requests are failing.",
            "resolution": "Fixed payment validation service.",
            "resolution_notes": "Application exception was corrected."
        },
        {
            "ticket_id": "INC002",
            "short_description": "Password reset not working",
            "description": "Users cannot reset their passwords.",
            "resolution": "Fixed email configuration.",
            "resolution_notes": "SMTP configuration was corrected."
        }
    ]

    embeddings = build_ticket_index(tickets)

    results = find_similar_tickets(
        "Payment service is failing",
        tickets,
        embeddings,
        top_k=2
    )

    assert results[0]["similarity"] >= results[1]["similarity"]


def test_top_k_limits_results():
    tickets = [
        {
            "ticket_id": "INC001",
            "short_description": "Payment API returning 500 errors",
            "description": "Payment requests are failing.",
            "resolution": "Fixed payment validation service.",
            "resolution_notes": "Application exception was corrected."
        },
        {
            "ticket_id": "INC002",
            "short_description": "Payment transaction failures",
            "description": "Customers cannot complete payments.",
            "resolution": "Database connection pool was increased.",
            "resolution_notes": "Connection pool had reached its limit."
        },
        {
            "ticket_id": "INC003",
            "short_description": "Password reset not working",
            "description": "Users cannot reset their passwords.",
            "resolution": "Fixed email configuration.",
            "resolution_notes": "SMTP configuration was corrected."
        }
    ]

    embeddings = build_ticket_index(tickets)

    results = find_similar_tickets(
        "Payment service is failing",
        tickets,
        embeddings,
        top_k=2
    )

    assert len(results) == 2