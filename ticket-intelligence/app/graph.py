from app.azure_vector_search import find_similar_tickets
from app.llm_service import normalize_ticket_language, analyze_with_history
from app.language_service import detect_language
from app.sla_analyzer import analyze_sla
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class TicketState(TypedDict, total=False):
    ticket: dict
    language: str
    is_english: bool
    normalized_text: str
    similar_tickets: list
    sla_analysis: dict
    final_analysis: str
    

def semantic_search_node(state: TicketState):
    similar_tickets = find_similar_tickets(
        state["normalized_text"],
        top_k=3
    )

    return {
        "similar_tickets": similar_tickets
    }

def sla_analysis_node(state: TicketState):
    sla_result = analyze_sla(state["ticket"])

    return {
        "sla_analysis": sla_result
    }
    

def detect_language_node(state: TicketState):
    result = detect_language(
        state["ticket"]["short_description"]
    )

    return {
        "language": result["language"],
        "is_english": result["is_english"]
    }
    

def route_after_language(state: TicketState):
    if state["is_english"]:
        return "english"

    return "translate"



def english_node(state: TicketState):
    return {
        "normalized_text": state["ticket"]["short_description"]
    }


def translate_node(state: TicketState):
    translated_text = normalize_ticket_language(
        state["ticket"],
        state["language"]
    )

    return {
        "normalized_text": translated_text
    }


def llm_analysis_node(state: TicketState):
    final_analysis = analyze_with_history(
        state["ticket"],
        state["similar_tickets"],
        state["sla_analysis"]
    )

    return {
        "final_analysis": final_analysis
    }


builder = StateGraph(TicketState)

builder.add_node("detect_language", detect_language_node)
builder.add_node("english", english_node)
builder.add_node("translate", translate_node)
builder.add_node("semantic_search", semantic_search_node)
builder.add_node("sla_analysis", sla_analysis_node)
builder.add_node("llm_analysis", llm_analysis_node)


builder.add_edge(START, "detect_language")

builder.add_conditional_edges(
    "detect_language",
    route_after_language,
    {
        "english": "english",
        "translate": "translate"
    }
)

# getting call first, then passing the result to the next node, every step has attached callback function
builder.add_edge("english", "semantic_search")
builder.add_edge("translate", "semantic_search")

builder.add_edge("semantic_search", "sla_analysis")
builder.add_edge("sla_analysis", "llm_analysis")
builder.add_edge("llm_analysis", END)

graph = builder.compile()



if __name__ == "__main__":
    ticket = {
        "ticket_id": "INC007",
        "short_description": "Customers are unable to complete payments because the payment service is failing",
        "priority": "P1",
        "status": "Open",
        "category": "Payment",
        "sla_hours": 4,
        "created_at": "2026-09-13T00:00:00",
        "resolved_at": None
    }

    result = graph.invoke({"ticket": ticket})

    print("Language:", result["language"])
    print("English:", result["is_english"])
    print("Normalized:", result["normalized_text"])
    print("Similar:", result["similar_tickets"])
    print("SLA:", result["sla_analysis"])
    print("Final Analysis:", result["final_analysis"])