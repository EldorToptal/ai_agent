from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


@tool("execute_python")
def execute_python_code(code: str) -> str:
    """Run Python code and return the result"""
    print("[Tool] execute_python_code is called!")
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return "Code executed successfully!"
    except Exception as e:
        return f"Error: {e}"


llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

agent = create_react_agent(llm, [execute_python_code])


def tester_node(state):
    message = [
        {"role": "user", "content": f"Test this Python code and response with PASS or FAIL: \n{state['code']}"}]
    response = agent.invoke({"messages": message})
    final_message = response["messages"][-1].content

    if "PASS" in final_message.upper():
        result = "PASS"
    elif "FAIL" in final_message.upper():
        result = "FAIL"
    else:
        result = "ERROR"

    return {"result": result, "details": final_message}
