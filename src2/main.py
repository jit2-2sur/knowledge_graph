from pathlib import Path

from load_html import load_html_files
from convert_json import htm_to_json
from load_graphdb import create_case_graph
from qna import get_cypher_query, run_cypher_query


def load_data(file_dir_path):
    html_files = Path(file_dir_path).glob('*.htm')

    for file in html_files:
        try:
            html_data = load_html_files(file)
            json_data = htm_to_json(html_data)
            create_case_graph(json_data)
        except Exception as e:
            print(f'Error occurred while processing {file}: {e}')


if __name__ == '__main__':
    # load data into graph
    file_dir_path = './data'
    load_data(file_dir_path)

    # perform Q&A using Cypher query
    question = input('Enter a question: ')
    cypher_query = get_cypher_query(question)
    result = run_cypher_query(cypher_query)
    if result != []:
        print('\n\nresult:', result[0][0])
    else:
        print('\n\nNo answer found.')