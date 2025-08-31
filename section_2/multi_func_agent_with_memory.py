import os
from typing import Dict
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

search_tool = DuckDuckGoSearchRun()


@tool
def multiply(a: int, b: int) -> int:
    """Ikkita butun sonni ko'paytirish"""
    return a * b


tools = [search_tool, multiply]

prompt = ChatPromptTemplate.from_messages([
    ("system", "Sen yordamchi agentsan. ReAct sifatida fikr yurit va faqat kerak bo'lganda vositalardan foydalanib, javob ber."),
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
    print(ask(session_id, "O'zbekistonning poytaxti qaysi?"))
    print(ask(session_id, "7 va 8 ni ko'paytirganda javobi nima bo'ladi?"))
    print(ask(session_id, "Mening ismim nima?"))
    # print(get_session_history(session_id))
