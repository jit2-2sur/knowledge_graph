import os
from dotenv import load_dotenv
from neomodel import (
    config,
    StructuredNode,
    StringProperty,
    DateProperty,
    RelationshipTo,
    RelationshipFrom,
    IntegerProperty
)


load_dotenv()
neo4j_url = os.getenv('NEO4J_URI_0')
config.DATABASE_URL = neo4j_url


class Court(StructuredNode):
    name = StringProperty(required=True)
    abbreviation = StringProperty()


class Case(StructuredNode):
    filename = StringProperty(unique_index=True, required=True)
    case_name = StringProperty(required=True)
    case_no = StringProperty()
    dated = DateProperty()
    judgement_date = DateProperty()
    result = StringProperty()
    full_text = StringProperty()
    pdf_link = StringProperty()

    # Relationships
    court = RelationshipTo('Court', 'HEARD_AT')
    coram = RelationshipTo('Judge', 'HEARD_BY')
    petitioner = RelationshipTo('Party', 'PETITIONED_BY')
    respondent = RelationshipTo('Party', 'RESPONDED_BY')
    acts = RelationshipTo('Act', 'GOVERNED_BY')
    citations = RelationshipTo('Citation', 'CITED_BY')
    counsel = RelationshipTo('Counsel', 'ARGUED_BY')


class Judge(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    cases = RelationshipFrom('Case', 'HEARD_BY')


class Party(StructuredNode):
    name = StringProperty(required=True)
    role = StringProperty()

    # Relationships
    petitioner_in_cases = RelationshipFrom('Case', 'PETITIONED_BY')
    respondent_in_cases = RelationshipFrom('Case', 'RESPONDED_BY')


class Act(StructuredNode):
    name = StringProperty(required=True)
    sections = StringProperty()

    # Relationships
    cases = RelationshipFrom('Case', 'GOVERNED_BY')


class Citation(StructuredNode):
    reference = StringProperty(unique_index=True, required=True)
    cases = RelationshipFrom('Case', 'CITED_BY')


class Counsel(StructuredNode):
    name = StringProperty(required=True)

    # Relationships
    cases = RelationshipFrom('Case', 'ARGUED_BY')
