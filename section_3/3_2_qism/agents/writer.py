import os
from typing import Dict
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


class WriterOutput(BaseModel):
    code: str = Field(description="Generated Python code")
    explanation: str = Field(description="Explanation of what the code does")


llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)


writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Python coding assistant. Generate clean, correct code."),
    ("human",
     "Write Python code for the following task: \n{task}\n The explain what the code does."),
])

writer_chain = writer_prompt | llm.with_structured_output(WriterOutput)


def writer_node(state):
    result: WriterOutput = writer_chain.invoke({"task": state['task']})
    return {"code": result.code, "explanation": result.explanation}
