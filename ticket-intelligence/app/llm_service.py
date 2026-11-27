import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    timeout=60.0,
    max_retries=3
)

model = os.getenv("AI_MODEL")

def summarize_ticket(ticket):
    prompt = f"""
        Analyze the following support ticket.

        Ticket ID: {ticket["ticket_id"]}
        Description: {ticket["short_description"]}
        Priority: {ticket["priority"]}
        Status: {ticket["status"]}
        Category: {ticket["category"]}

        Provide:
        1. A short summary
        2. The likely issue
        3. The potential impact
    """

    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text



def analyze_with_history(ticket, similar_tickets, sla_analysis):
    history = ""

    for similar in similar_tickets:
        for similar in similar_tickets:
            history += f"""
                Historical Ticket: {similar["ticket_id"]}
                Issue: {similar["description"]}
                Score: {similar["score"]:.2f}
                Resolution: {similar["resolution"]}
                Resolution Notes: {similar["resolution_notes"]}
                """

    prompt = f"""
            You are an IT support ticket analysis assistant.

            Analyze the new ticket using the historical tickets provided below.

            NEW TICKET
            Ticket ID: {ticket["ticket_id"]}
            Description: {ticket["short_description"]}
            Priority: {ticket["priority"]}
            Category: {ticket["category"]}

            HISTORICAL TICKETS
            {history}
            
            SLA ANALYSIS
            SLA Hours: {sla_analysis["sla_hours"]}
            Elapsed Hours: {sla_analysis["elapsed_hours"]}
            Remaining Hours: {sla_analysis["remaining_hours"]}
            SLA Breached: {sla_analysis["sla_breached"]}

            Provide:

                1. A concise summary of the new ticket.
                2. The likely root cause based ONLY on evidence from the historical tickets.
                3. The potential business impact.
                4. Recommended next action based on previous resolutions.
                5. Mention which historical ticket is most relevant.
                6. Explain how the historical resolution relates to the new ticket.
                7. Explain the SLA status of the ticket.

            Important:
                - Do not invent a root cause that is not supported by the historical tickets.
                - Clearly distinguish between historical evidence and assumptions.
                - If the historical tickets do not provide enough evidence to determine the root cause, say so.
            """
    
    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text


def normalize_ticket_language(ticket, language):
    if language == "en":
        return ticket["short_description"]

    prompt = f"""
        Translate the following IT support ticket into clear English.

        Ticket:
        {ticket["short_description"]}

        Return only the translated ticket text.
    """

    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text.strip()