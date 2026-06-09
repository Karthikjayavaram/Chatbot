from typing_extensions import TypedDict,Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()


llm = HuggingFaceEndpoint(  
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    max_new_tokens=1024,
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)
# this is state 
class chatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
# this is node (Single Node)
def chat_node(state: chatState):
    messages=state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

checkpointer = InMemorySaver()

graph = StateGraph(chatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

