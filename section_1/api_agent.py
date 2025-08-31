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
tools = [search_tool]

prompt = ChatPromptTemplate.from_messages([
    ("system", "Sen yordamchi agentsan. ReAct sifatida fikr yurit va faqat kerak bo'lganda vositalardan foydalanib, javob ber."),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent_runnable = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent = AgentExecutor(agent=agent_runnable, tools=tools)

if __name__ == "__main__":
    out = agent.invoke(
        {"input": "Toshkentda issiqlik nechi gradus?"})
    print(out['output'])
