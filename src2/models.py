from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
)


# Case Node
class Case(StructuredNode):
    case_name = StringProperty()
    case_no = StringProperty(required=True)
    result = StringProperty()
    overruled = StringProperty()
    overruled_by = StringProperty()

    appealed_case = RelationshipTo("AppealedCase", "Appeal_to")
    court_data = RelationshipTo("CourtData", "Has_data")
    summary_data = RelationshipTo("SummaryData", "Has_data")
    citations_data = RelationshipTo("CitationsData", "Has_data")


# Court Node
class Court(StructuredNode):
    court_name = StringProperty()
    court_abbreviation = StringProperty()

    cases = RelationshipTo("Case", "Is_case")
    appealed_cases = RelationshipTo("AppealedCase", "Is_case")


# AppealedCase Node
class AppealedCase(StructuredNode):
    case_name = StringProperty()
    case_no = StringProperty(required=True)
    result = StringProperty()
    overruled = StringProperty()
    overruled_by = StringProperty()

    original_case = RelationshipFrom("Case", "Appeal_from")


# CourtData Node
class CourtData(StructuredNode):
    case_type = StringProperty()
    petitioner = StringProperty()
    respondent = StringProperty()
    coram = StringProperty()
    petitioner_counsel = StringProperty()
    respondent_counsel = StringProperty()
    act = StringProperty()
    bench = StringProperty()
    dated = StringProperty()
    reportable = StringProperty()
    case_no = StringProperty(required=True)

    neighbouring_data = RelationshipTo("CitationsData", "Neighbouring_data")
    neighbouring_summary = RelationshipTo("SummaryData", "Neighbouring_data")


# SummaryData Node
class SummaryData(StructuredNode):
    case_no = StringProperty(required=True)
    evidence = StringProperty()
    conclusion = StringProperty()
    courts_reasoning = StringProperty()
    precedent_analysis = StringProperty()
    legal_analysis = StringProperty()
    respondents_arguments = StringProperty()
    petitioners_arguments = StringProperty()
    issues = StringProperty()
    facts = StringProperty()
    summary = StringProperty()

    neighbouring_court = RelationshipTo("CourtData", "Neighbouring_data")
    neighbouring_citations = RelationshipTo("CitationsData", "Neighbouring_data")


# CitationsData Node
class CitationsData(StructuredNode):
    case_no = StringProperty(required=True)
    citations = StringProperty()
    cited = StringProperty()
    headnotes = StringProperty()
    case_referred = StringProperty()
    keywords = StringProperty()

    neighbouring_summary = RelationshipTo("SummaryData", "Neighbouring_data")
    neighbouring_court = RelationshipTo("CourtData", "Neighbouring_data")
