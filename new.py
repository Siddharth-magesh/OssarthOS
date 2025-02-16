from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(
  model="llama3.1:8b",
  keep_alive=-1,
  temperature=0,
  max_new_tokens=512    
)

prompt = ChatPromptTemplate.from_template("Write me a 500 word article on {topic} from the perspective of a profession")

chain = prompt | llm | StrOutputParser()

# print(chain.invoke({"topic": "LLMs","profession":"shipping magnate"}))

for chunk in chain.stream({"topic":"LLMs","profession":"shipping magnate"}):
    print(chunk,end="",flush=True)