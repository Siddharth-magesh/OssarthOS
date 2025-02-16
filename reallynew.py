from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel , Field
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser

class Person(BaseModel):
    name: str = Field(description="The person's name",required=True)
    height: str = Field(description="The person's height",required=True)
    hair_color: str = Field(description="The person's hair color")

context ="""Alex is 5 feet tall.
Claudia is 1 feet taller than Alex and jumps higher than him.
Claudia is a brunette and Alex is blonde.
"""

prompt = PromptTemplate.from_template(
    """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    you are a smart assistant take the following context and question below and return your answer is JSON.
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    QUESTION: {question} \n
    CONTEXT: {context} \n
    JSON:
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
"""
)

llm = OllamaFunctions(
    model="phi3:14b",
    format="json",
    temperature=0
)

structured_llm = llm.with_structured_output(Person)
chain = prompt | structured_llm

response = chain.invoke({
    "question":"Who is taller?",
    "context":context
})

print(response)