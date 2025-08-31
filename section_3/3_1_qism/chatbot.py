import os
from typing import Dict
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

emb = OpenAIEmbeddings(model='text-embedding-3-small')

persist_directory = "./chroma_db"

if not os.path.exists(persist_directory):
    raise FileNotFoundError(
        f"Vector database not found at {persist_directory}. Run db_build.py first!")

vs = Chroma(embedding_function=emb, collection_name="customer_db",
            persist_directory=persist_directory)

retriever = vs.as_retriever(search_kwargs={"k": 3})


@tool
def db_search(text: str) -> str:
    """Mijoz savollariga javob berish uchun knowledge base dan qidirish"""
    res = retriever.invoke(text)
    if not res:
        return "Hech narsa topilmadi!"
    return "\n\n".join([f"{d.page_content}" for d in res])


tools = [db_search]

prompt = ChatPromptTemplate.from_messages([
    ("system", "Siz mijozlarga xizmat ko'rsatish chatbotsiz. Faqat mavjud manbalardan foydalanib javob bering. Agar topilmasa, to'grisini ayting."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent_runnable = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent = AgentExecutor(agent=agent_runnable, tools=tools, verbose=False)

_store: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


agent_with_memory = RunnableWithMessageHistory(
    agent,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


def ask(session_id: str, text: str) -> str:
    cfg = {"configurable": {"session_id": session_id}}
    result = agent_with_memory.invoke({"input": text}, config=cfg)
    return result.get('output', str(result))


if __name__ == "__main__":
    session_id = 'eldor'
    print(ask(session_id, "Salom, mening ismim Eldor"))
    print(ask(session_id, "Sizga mahsulotni qanday va qachon qaytarsam bo'ladi?"))
