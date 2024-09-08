import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from neomodel import db, config


load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
url = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
neo4j_url = os.getenv('NEO4J_URI_0')


prompt_template = """A user asked a question related to a legal case. Now to answer the question we need to search through graph database. here is the graph schema:
graph_schema: {graph_schema}

Atfirst, you need to extract if any of these properties are present in the user question. if present then get those property and value
Then, write a cypher queery to retrieve the answer. Follow the graph node name, relationship name, property name properly according to schema. Only return the cypher query.

you have retrieved the following information from user question for writing the query,
question_information:{question}
cypher query:
"""


def get_cypher_query(question):
    llm = GoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=google_api_key)
    graph = Neo4jGraph(url=url, username=username, password=password)
    # graph = Neo4jGraph(url=url, username=username, password=password, database= database)

    # Create a prompt template
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["graph_schema", "question"],
    )

    # Create the LLM chain
    chain = prompt | llm

    cypher_query = chain.invoke({"graph_schema": graph.schema, "question": question})
    print(cypher_query)
    return cypher_query[10:-4]


def run_cypher_query(cypher_query):
    config.DATABASE_URL = neo4j_url
    results, meta = db.cypher_query(cypher_query)
    print('result: ',results)
    return results
