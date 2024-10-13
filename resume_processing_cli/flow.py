
from typing import Annotated, Literal, TypedDict
import os

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, Graph

from agents import *

from dotenv import load_dotenv

load_dotenv()

langsmith_api= os.environ.get("LANGSMITH_API_KEY")
gemini_api = os.environ.get("GEMINI_API_KEY")


def human_call(data):
    print(f"Response : {data} " )
    op = input("enter ")
    # op = st.text_input("Provide your response on it: ")
    result = f"correction on this is {op} for given data {data}"
    return result



# Define logic that will be used to determine which conditional edge to go down
# def reader_should_continue(data):
#     print(type(data))
#     if data == "Unsupported file format. Please provide a PDF or DOCX file."  or "invalid" in  data.lower() or data == "No text found" :
#         print("detected no text or unsupported or conditions")
#         return "human"
#     else :
#         return "continue"
def reader_should_continue(data):
    print(type(data))
    
    # Check if data is a string first, to safely use .lower()
    if isinstance(data, str):
        if data == "Unsupported file format. Please provide a PDF or DOCX file." or "invalid" in data.lower() or data == "No text found" or "not" in data:
            print("detected no text or unsupported conditions")
            return "human"
    else:
        # If data is a dictionary (JSON structure), handle the case where "invalid" appears in the values
        # Recursively check for the word "invalid" in the dictionary
        def contains_invalid(value):
            if isinstance(value, dict):
                return any(contains_invalid(v) for v in value.values())
            if isinstance(value, str):
                return "invalid" in value.lower()
            return False

        if contains_invalid(data):
            print("detected invalid in JSON structure")
            return "human"
    
    return "continue"


workflow = Graph()


workflow.add_node("reader", reader)
workflow.add_node("extractor", extractor)
workflow.add_node("validator", validator)
workflow.add_node("human_call", human_call)


workflow.set_entry_point("reader")
workflow.add_edge("reader","extractor")
# workflow.add_conditional_edges(
#     "human_call",
#     reader_should_continue,
#     {
#         "continue": "extractor",
#         "human": "human_call"
#         , END: END
#     }
# )
workflow.add_edge('extractor', 'validator')

workflow.add_conditional_edges(
    "validator",
    reader_should_continue,
    {
        
        "human": "human_call",
        "continue": END ,
         END: END
    }
)

workflow.add_edge("human_call","extractor")

chain = workflow.compile()
result = chain.invoke("sample2.pdf")
# def process_pdf():
#     result = chain.invoke("sample2.pdf")
#     print(result)
#output = result['agent_outcome'].return_values["output"]
print("result ",result)

# process_pdf()
