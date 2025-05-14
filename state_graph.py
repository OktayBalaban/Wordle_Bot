from langgraph.graph import StateGraph
from nodes import start, get_state, submit_guess, check_result, ask_llm_guess, end

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("Start", start)
    graph.add_node("Get State", get_state)
    graph.add_node("Ask Guess", ask_llm_guess)
    graph.add_node("Submit Guess", submit_guess)
    graph.add_node("Check Result", check_result)
    graph.add_node("End", end)

    graph.add_edge("Start", "Get State")
    graph.add_edge("Get State", "Ask Guess")
    graph.add_edge("Ask Guess", "Submit Guess")
    graph.add_edge("Submit Guess", "Check Result")
    graph.add_conditional_edges(
        "Check Result",
        lambda state: state["route"],
        {
            "End": "End",
            "Get State": "Get State"
        }
    )

    graph.set_entry_point("Start")
    graph.set_finish_point("End")

    return graph.compile()
