import os
import json
import urllib.parse
import urllib.request
from typing import Dict
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0,
                 timeout=30, max_retries=1)


def _fx_convert_impl(amount: float, base: str, target: str) -> dict:
    base_up, target_up = base.upper(), target.upper()
    url = f"https://open.er-api.com/v6/latest/{base_up}"

    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read())

    rate = data['rates'][target_up]
    result = rate * amount

    return {
        "base": base_up,
        "target": target_up,
        "amount": amount,
        "rate": rate,
        "result": result,
        "date": data['time_last_update_utc']
    }


@tool
def fx_convert(amount: float, base: str, target: str) -> str:
    """Convert currency amount from base to target using Exchange Rate API"""
    try:
        res = _fx_convert_impl(amount, base, target)
        return (
            f"{res['amount']} {res['base']} = {res['result']} {res['target']}"
            f"(rate {res['rate']}, date {res['date']})"
        )
    except Exception as e:
        return f"Conversion failed: {e}"


currency_tool = [fx_convert]
currency_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the Currency Agent. ONLY handle currency coversions using fx_convert tool. Be concise and factual.",),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])


currency_agent_runnable = create_tool_calling_agent(
    llm=llm, tools=currency_tool, prompt=currency_prompt)

currency_agent = AgentExecutor(agent=currency_agent_runnable, tools=currency_tool,
                               max_iterations=3)


# ==============================================================================

wiki_api = WikipediaAPIWrapper(
    lang="en", top_k_results=2, doc_content_chars_max=1200)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api)

travel_tool = [wiki_tool]
travel_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the travel Guide Agent. Fetch concise, travel-relevant facts and tips using Wikipedia. Focus on highlights, neighborhoods, transport, must-see spots.",),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

travel_agent_runnable = create_tool_calling_agent(
    llm=llm, tools=travel_tool, prompt=travel_prompt)

travel_agent = AgentExecutor(agent=travel_agent_runnable, tools=travel_tool,
                             max_iterations=3)

# ==============================================================================


@tool
def currency_agent_tool(task: str) -> str:
    """Delegate currency-related tasks (amount/base/target)  in the Currency Agent."""
    out = currency_agent.invoke({"input": task})
    return out.get("output", str(out))


@tool
def travel_agent_tool(task: str) -> str:
    """Delegate destination information queries in the Travel Guide Agent."""
    out = travel_agent.invoke({"input": task})
    return out.get("output", str(out))


coord_tools = [currency_agent_tool, travel_agent_tool]

coord_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the Coordinator Agent. Understand the user's goal, then call the right role agent(s)."
     "Use currency_agent_tool for any currency conversions."
     "Use travel_agent_tool for destination info."
     "If both are needed, call both and produce a single, well-structured answer."
     "Remember user preferences from the conversation."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

coord_agent_runnable = create_tool_calling_agent(
    llm=llm, tools=coord_tools, prompt=coord_prompt)

coord_agent = AgentExecutor(agent=coord_agent_runnable, tools=coord_tools)


_store: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


agent_with_memory = RunnableWithMessageHistory(
    coord_agent,
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
    print(ask(session_id, "Parijdagi qaysi muzeyni tavsiya qilasiz? Sayohat uchun 500 USD bor, EURda qancha bo'ladi?"))
    # print(ask(session_id, "Sayohat uchun 500 USD bor, EURda qancha bo'ladi?"))
