from datetime import datetime


def analyze_sla(ticket):    
    
    created_at = datetime.fromisoformat(ticket["created_at"])
    
    sla_hours = ticket["sla_hours"]

    if ticket["resolved_at"]:
        end_time = datetime.fromisoformat(ticket["resolved_at"])
    else:
        end_time = datetime.now()
    
    elapsed_hours = (end_time - created_at).total_seconds() / 3600

    sla_breached = elapsed_hours > sla_hours

    remaining_hours = max(sla_hours - elapsed_hours, 0)

    return {
        "ticket_id": ticket["ticket_id"],
        "sla_hours": sla_hours,
        "elapsed_hours": round(elapsed_hours, 2),
        "remaining_hours": round(remaining_hours, 2),
        "sla_breached": sla_breached
    }
