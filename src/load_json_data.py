import os
import json
from pathlib import Path
from neomodel import config
from dotenv import load_dotenv
from datetime import datetime

from model2 import (
    Case, Court, ApplealedCase, CourtData, SummaryData, CitationsData
)

# Load environment variables
load_dotenv()
neo4j_url = os.getenv('NEO4J_URI_0')
config.DATABASE_URL = neo4j_url


def load_to_graphdb(case_data):
    try:
        # Convert date strings to datetime.date objects
        dated = convert_date(case_data['dated'])
        judgement_date = convert_date(case_data['judgement_date'])

        # Create or Get Court Node
        court = Court.nodes.first_or_none(name=case_data['court'])
        if not court:
            court = Court(name=case_data['court'], abbreviation=case_data['abbr']).save()

        # Create Case Node
        case = Case(
            filename=case_data['filename'],
            case_name=case_data['casename'],
            case_no=case_data['caseno'],
            dated=dated,
            judgement_date=judgement_date,
            result=case_data['result'],
            pdf_link=case_data['pdf_link']
        ).save()

        # Create Relationship between Case and Court
        case.court.connect(court)

        # Create or Get Judge Nodes and Relationships
        for judge_name in json.loads(case_data['coram']):
            judge = Judge.nodes.first_or_none(name=judge_name)
            if not judge:
                judge = Judge(name=judge_name).save()
            case.coram.connect(judge)

        # Create or Get Counsel Nodes and Relationships
        if case_data.get('counsel'):
            for counsel_name in case_data['counsel'].split(","):
                counsel_name = counsel_name.strip()
                counsel = Counsel.nodes.first_or_none(name=counsel_name)
                if not counsel:
                    counsel = Counsel(name=counsel_name).save()
                case.counsel.connect(counsel)

        # Create or Get Act Nodes and Relationships
        if case_data.get('act'):
            acts = json.loads(case_data['act'])
            for act_name, sections in acts.items():
                act = Act.nodes.first_or_none(name=act_name)
                if not act:
                    act = Act(name=act_name, sections=str(sections)).save()
                case.acts.connect(act)
        print('.......')
    except Exception as e:
        print('data load to database failed.', e)


def load_json_files(data_dir):
    print('Starting...')
    json_files = Path(data_dir).glob('*.json')

    for file in json_files:
        print(f'Processing file: {file}')
        with open(file, 'r') as f:
            try:
                case_data = json.load(f)
                print('json load done')
                load_to_graphdb(case_data)
            except Exception as e:
                print('file not opened', e)


if __name__ == "__main__":
    data_dir = './data'
    load_json_files(data_dir)
    print('Done')
