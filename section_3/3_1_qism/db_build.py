from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
import os

load_dotenv()

sources = [
    TextLoader('data/refund_policy.txt').load(),
    TextLoader('data/support_info.txt').load(),
    TextLoader('data/working_hours.txt').load(),
]

docs = [d for sub in sources for d in sub]

emb = OpenAIEmbeddings(model='text-embedding-3-small')

persist_directory = "./chroma_db"
os.makedirs(persist_directory, exist_ok=True)

vs = Chroma.from_documents(
    docs, emb, collection_name="customer_db", persist_directory=persist_directory)
