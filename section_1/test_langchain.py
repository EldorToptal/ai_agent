from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv()

llm = ChatOpenAI(model_name="gpt-5-mini", temperature=1)

response = llm([HumanMessage(content="Salom, AI agent nima?")])
print(response)
