import json


def load_tickets():
    with open("data/tickets.json", "r") as file:
        return json.load(file)
    

def analyze_ticket(ticket):
    return {
        "ticket_id": ticket["ticket_id"],
        "priority": ticket["priority"],
        "category": ticket["category"],
        "is_high_priority": True if ticket["priority"] == "P1" else False
    }