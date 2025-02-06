
from Models.llm import LLM
from Models.prompt import PROMPT
from langgraph.graph import StateGraph, START, END
from Models.state import State
from Models.assistant import Assistant
from Models.tools import *
from langgraph.prebuilt import MemorySaver, tools_condition
import uuid
import os

HF_API_KEY = os.environ.get("HF_API_KEY")
REPO_ID = os.environ.get("REPO_ID")

def main():
    llm = LLM(HF_API_KEY, REPO_ID, max_new_tokens=256, temperature=0.7)
    tools = TOOLS
    prompt = PROMPT

    RUNNABLE = prompt | llm.bind_tools(tools)

    builder = StateGraph(State)
    builder.add_node("assistant", Assistant(RUNNABLE))
    builder.add_node("tools", create_tool_node_with_fallback(tools))

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)  # Move to tools after input
    builder.add_edge("tools", "assistant")  # Return to assistant after tool execution
    
    memory = MemorySaver()
    graph = builder.compile(memory=memory)

    graph.get_graph().visual_graph.save("graph.png")

    # Let's create an example conversation a user might have with the assistant
    tutorial_questions = [
        'hey',
        'can you calculate my energy saving',
        "my montly cost is $100, what will i save"
    ]

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    _printed = set()
    for question in tutorial_questions:
        events = graph.stream(
            {"messages": ("user", question)}, config, stream_mode="values"
        )
        for event in events:
            _print_event(event, _printed)



if __name__ == "__main__":
    main()