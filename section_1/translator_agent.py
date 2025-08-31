from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model_name="gpt-5-mini", temperature=1)

template = "Matnni o'zbek tiliga tarjima qiling: \n{english}"

prompt = PromptTemplate(input_variables=["english"], template=template)

chain = prompt | llm

output = chain.invoke(
    'LangChain is a framework for developing applications powered by large language models (LLMs).')

print(output)
