from pathlib import Path
from langchain_community.document_loaders import BSHTMLLoader

import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer

from model2 import (
    Case, Court, AppealedCase, CourtData, SummaryData, CitationsData
)


load_dotenv()
url = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
google_api_key = os.getenv('GOOGLE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
database = 'htmldb2'


# graph
graph = Neo4jGraph(url=url, username=username, password=password, database=database)
graph.refresh_schema()


def load_html_files(data_dir):
    print('Starting...')
    html_files = Path(data_dir).glob('*.htm')

    for file in html_files:
        print(f'Processing file: {file}')
        loader = BSHTMLLoader(file)
        try:
            data = loader.load()
            # print(data[0].page_content)
            # print(data[0].metadata['source'])
            # printing only first 100 char of content
            # print(data[0].page_content[0:100])

            # converting to graph data
            # convert_to_graph(data)
            convert_to_graph_new(data)
        except Exception as e:
            print('error in loading file ', e)


def convert_to_graph(data):
    llm = GoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=google_api_key)
    llm_transformer = LLMGraphTransformer(llm=llm)
    try:
        graph_data = llm_transformer.convert_to_graph_documents(data)
        graph.add_graph_documents(graph_data)
        # print(f"Nodes:{graph_data[0].nodes}")
        # print(f"Relationships:{graph_data[0].relationships}")
    except Exception as e:
        print('error in converting graph ', e)


def convert_to_graph_filtered(data):
    llm = GoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=google_api_key)

    llm_transformer_filtered = LLMGraphTransformer(
        llm=llm,
        allowed_nodes=[
            'Case', 'Court', 'ApplealedCase', 'CourtData', 'SummaryData', 'CitationsData',
            'Person', 'Location', 'Object', 'Event', 'Law'
        ],
        allowed_relationships=[
            'Appeal_from', 'Appeal_to', 'Is_case', 'Has_data', 'Neighbouring_data',
            'Convicted_of', 'Sentenced_to', 'works_for', 'Concerning', 'Filed_by', 'Investigated_by',
            'petetioned_by', 'petetioned_against', 'ordered_by'
        ],
        node_properties=[
            'case_name', 'case_no', 'result', 'overruled', 'overruled_by',
            'courst_name', 'Court_abbreviation',
            'type_of_case', 'petetioner', 'respondent', 'coram', 'petetioner_counsel',
            'respondent_counsel', 'act', 'bench', 'dated', 'reportable',
            'citations', 'cited', 'headnotes', 'case_referred', 'keywords',
            'evidence', 'conclusion', 'courts_reasoning', 'precedent_analysis',
            'legal_analysis',  'respondents_arguments', 'petitioners_arguments',
            'issues', 'facts', 'summary'
        ]
    )

    try:
        graph_data = llm_transformer_filtered.convert_to_graph_documents(data)
        graph.add_graph_documents(graph_data)
        # print(f"Nodes:{graph_data[0].nodes}")
        # print(f"Relationships:{graph_data[0].relationships}")
    except Exception as e:
        print('error in converting graph ', e)


def convert_to_graph_new(data):
    llm = GoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=google_api_key)

if __name__ == '__main__':
    # load_html_files('C:\\Users\\admin\\Downloads\\Aritra-Docs\\Aritra-Docs')
    load_html_files('./html_data')
    graph._driver.close()
