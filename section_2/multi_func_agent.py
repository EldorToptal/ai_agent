import os
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_tool_calling_agent, AgentExecutor
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
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent_runnable = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent = AgentExecutor(agent=agent_runnable, tools=tools)

if __name__ == "__main__":
    out = agent.invoke(
        {"input": "Salom, mening ismim Eldor"})
    print(out['output'])
    out = agent.invoke(
        {"input": "O'zbekistonning poytaxti qaysi?"})
    print(out['output'])
    out = agent.invoke(
        {"input": "7 va 8 ni ko'paytirganda javobi nima bo'ladi?"})
    print(out['output'])
    out = agent.invoke(
        {"input": "Mening ismim nima?"})
    print(out['output'])
