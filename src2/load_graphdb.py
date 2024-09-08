import os
from dotenv import load_dotenv
from neomodel import config, db
from neomodel.exceptions import UniqueProperty

from models import Case, Court, AppealedCase, CourtData, SummaryData, CitationsData

# Load environment variables
load_dotenv()
neo4j_url = os.getenv("NEO4J_URI_0")
config.DATABASE_URL = neo4j_url


# Function to create or get a node (avoiding duplication)
def get_or_create_node(model, **properties):
    try:
        node = model.nodes.get(**properties)
        return node
    except model.DoesNotExist:
        node = model(**properties).save()
        return node
    except UniqueProperty:
        return None


# Function to create nodes and relationships from extracted JSON data
def create_case_graph(case_info):
    # Create or retrieve the Court node
    court = get_or_create_node(
        Court,
        court_name=case_info["court_name"],
        court_abbreviation=case_info["court_abbreviation"],
    )

    # Create or retrieve the Case node
    case = get_or_create_node(
        Case,
        case_name=case_info["case_name"],
        case_no=case_info["case_no"],
        result=case_info["result"],
        overruled=str(case_info["overruled"]),
        overruled_by=case_info["overruled_by"],
    )

    # Create relationship between Court and Case (Is_case)
    if court and case:
        court.cases.connect(case)

    # Create CourtData node
    court_data = get_or_create_node(
        CourtData,
        case_no=case_info["case_no"],
        case_type=case_info["case_type"],
        petitioner=case_info["petitioner"],
        respondent=case_info["respondent"],
        coram=case_info["coram"],
        petitioner_counsel=case_info["petitioner_counsel"],
        respondent_counsel=case_info["respondent_counsel"],
        act=case_info["act"],
        bench=case_info["bench"],
        dated=case_info["dated"],
        reportable=str(case_info["reportable"]),
    )

    # Create relationship between Case and CourtData (Has_data)
    if case and court_data:
        case.court_data.connect(court_data)

    # Create SummaryData node
    summary_data = get_or_create_node(
        SummaryData,
        case_no=case_info["case_no"],
        evidence=case_info["evidence"],
        conclusion=case_info["conclusion"],
        courts_reasoning=case_info["courts_reasoning"],
        precedent_analysis=case_info["precedent_analysis"],
        legal_analysis=case_info["legal_analysis"],
        respondents_arguments=case_info["respondents_arguments"],
        petitioners_arguments=case_info["petitioners_arguments"],
        issues=case_info["issues"],
        facts=case_info["facts"],
        summary=case_info["summary"],
    )

    # Create relationship between Case and SummaryData (Has_data)
    if case and summary_data:
        case.summary_data.connect(summary_data)

    # Create CitationsData node
    citations_data = get_or_create_node(
        CitationsData,
        case_no=case_info["case_no"],
        citations=case_info["citations"],
        cited=case_info["cited"],
        headnotes=case_info["headnotes"],
        case_referred=case_info["case_referred"],
        keywords=case_info["keywords"],
    )

    # Create relationship between Case and CitationsData (Has_data)
    if case and citations_data:
        case.citations_data.connect(citations_data)

    # Create Neighbouring_data relationships between related data nodes
    if citations_data and court_data:
        citations_data.neighbouring_court.connect(court_data)
        court_data.neighbouring_data.connect(citations_data)
    if citations_data and summary_data:
        citations_data.neighbouring_summary.connect(summary_data)
        summary_data.neighbouring_citations.connect(citations_data)
    if summary_data and court_data:
        summary_data.neighbouring_court.connect(court_data)
        court_data.neighbouring_summary.connect(summary_data)

    print(f"Graph data for case {case_info['case_name']} created successfully.")
