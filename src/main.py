import os
from dotenv import load_dotenv
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.graphs import Neo4jGraph
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate


load_dotenv()
url_0 = os.getenv('NEO4J_URI_0')
url = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
google_api_key = os.getenv('GOOGLE_API_KEY')
database = 'neo4j'


graph = Neo4jGraph(url=url, username=username, password=password, database=database)
graph.refresh_schema()
#print(graph.schema)


# setup llm model
llm = GoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=google_api_key)

CYPHER_GENERATION_TEMPLATE = """
Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Relationship between information for additional reference:
('Case', 'ARGUED_BY', 'Councel'),
('Case', 'CITED_BY', 'Citation'),
('Case', 'GOVERNED_BY', 'Act'),
('Case', 'PETITIONED_BY', 'Party'),
('Case', 'RESPONDED_BY', 'Party'),
('Case', 'HEARD_BY', 'Judge'),
('Court', 'HEARD_AT', 'Case'),
('Judge', 'HEARD_BY', 'Case'),
('Party', 'PETITIONED_BY', 'Case'),
('Party', 'RESPONDED_BY', 'Case'),
('Act', 'GOVERNED_BY', 'Case'),
('Citation', 'CITED_BY', 'Case'),
('Counsel', 'ARGUED_BY', 'Case')

Cypher examples:
# Cases related to Delhi High Court
MATCH (c:Case)-[:HEARD_AT]->(court:Court {name: 'Delhi High Court'})
RETURN c.case_name AS case_name, c.case_no AS case_no, c.judgement_date AS judgement_date

# who was judge for the Salman Salim Khan case
MATCH (c:Case {case_name: 'Salman Salim Khan Vs The State Of Maharashtra'})-[:HEARD_BY]->(j:Judge)
RETURN j.name AS judge_name

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
If the cypher query didn't generate any response, try more queries.

The question is:
{question}
"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

# chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True, cypher_prompt=CYPHER_GENERATION_PROMPT)
chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True,)
# response = chain.invoke({"query": "cases associated with Delhi High Court"})
response = chain.run("""5 cases associated with court named Delhi High Court""")
print(response)

response = chain.run("""judge name(j.name) for the case named 'Salman Salim Khan Vs The State Of Maharashtra'""")
print(response)

response = chain.run("""coumcel name for the case named 'Salman Salim Khan Vs The State Of Maharashtra'""")
print(response)

response = chain.run("""act or law associated with the case named 'Salman Salim Khan Vs The State Of Maharashtra'""")
print(response)

graph._driver.close()
