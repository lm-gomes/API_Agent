from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Literal

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0)


class PromptType(TypedDict):
    type: Literal['internet_support', 'non_internet_support']

class MyState(TypedDict):
    message: str
    summary: str = ""
    answer: str

def summary_to_model(state: MyState):
    if(state.get("summary", "") == ""):
        summary = model.invoke([{"role": "user", "content": state['message']}]).content
    else:
        summary = model.invoke([{"role": "user", "content": f"Prompt atual: {state['message']}\nResumo da conversa até agora: {state['summary']}\nBaseado nessa conversa, crie um resumo levando em consideração os dados mais importantes."}]).content
    print(summary)
    return {"summary":summary}

def output(state: MyState):
    answer = model.invoke([{"role": "system", "content": f"Resumo da conversa: {state['summary']}"}, {"role": "user", "content": state['message']}])
    return {"answer": answer, "summary":state['summary']}


graph = StateGraph(state_schema=MyState)

graph.add_node("summary", summary_to_model)
graph.add_node("output", output)

graph.add_edge(START, "summary")
graph.add_edge("summary", "output")
graph.add_edge("output", END)

graph_compiled = graph.compile()

graph_compiled.invoke({"message": "Olá, tudo bem? Meu nome é Lucas"}, {"configurable": {"thread_id": "1"}})
graph_compiled.invoke({"message": "Olá, sabe meu nome?"}, {"configurable": {"thread_id": "1"}})

