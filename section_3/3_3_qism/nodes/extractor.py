from typing import Dict
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from schemas import ResumeExtract

extract_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert HR analyst. Extract structured info from the resume text."),
    ("human", "Resume text:\n```\n{resume_text}\n```\n\n Return a structured summary with: name, summary, years_experience (float if possible), skills (list of normalized lowercase strings), education (short), recent_companies (list), projects (list).")
])

_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

extract_chain = extract_prompt | _llm.with_structured_output(ResumeExtract)


def extractor_node(state: Dict) -> Dict:
    """
    Input:
        state["resume_text"] -> text
    Output:
        {"extracted": ResumeExtract}
    """
    extracted: ResumeExtract = extract_chain.invoke(
        {"resume_text": state['resume_text']})
    return {"extracted": extracted}
