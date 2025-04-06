import chainlit as cl
from app.vectorstore import VECTOR_STORE
from app.llm import LLM
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph
from langgraph.graph.message import START
from langgraph.checkpoint import InMemorySaver


PROMPT = PromptTemplate.from_template(
    "Answer the following question using the context below.\n\n{context}\n\nQuestion: {question}"
)

class State(dict):
    question: str
    context: list
    answer: str

@tool
def retrieve(q: str):
    docs = VECTOR_STORE.similarity_search(q, k=5)
    return "\n\n".join([f"## Source: {doc.metadata['source']}\n{doc.page_content}" for doc in docs])

def retrieve_state(state):
    results = VECTOR_STORE.similarity_search(state["question"], k=5)
    return {"context": results}

def generate_state(state):
    context = "\n\n".join(doc.page_content for doc in state["context"])
    prompt = PROMPT.format(question=state["question"], context=context)
    response = LLM.invoke(prompt)
    return {"answer": response.content}

graph = StateGraph(State).add_sequence([retrieve_state, generate_state])
graph.add_edge(START, "retrieve_state")
compiled = graph.compile()

@cl.on_message
async def on_message(message: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    response = compiled.invoke({"question": message.content})
    await cl.Message(content=response["answer"]).send()
