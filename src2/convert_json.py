import os
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Define the CaseInfo Pydantic model
class CaseInfo(BaseModel):
    case_name: str = Field(description="The name of the case")
    case_no: str = Field(description="The case number")
    result: str = Field(description="The result of the case", default=None)
    overruled: bool = Field(description="Whether the case was overruled", default=None)
    overruled_by: str = Field(
        description="The case that overruled this case", default=None
    )
    court_name: str = Field(description="The name of the court", default=None)
    court_abbreviation: str = Field(
        description="Abbreviation of the court name", default=None
    )
    case_type: str = Field(description="The type of the case", default=None)
    petitioner: str = Field(description="The petitioner in the case", default=None)
    respondent: str = Field(description="The respondent in the case", default=None)
    coram: str = Field(
        description="The coram (judicial bench) of the case", default=None
    )
    petitioner_counsel: list = Field(
        description="The counsel for the petitioner", default=None
    )
    respondent_counsel: list = Field(
        description="The counsel for the respondent", default=None
    )
    act: list = Field(description="The relevant act or legislation", default=None)
    bench: list = Field(description="The bench of the court", default=None)
    dated: str = Field(description="The date of the case", default=None)
    reportable: bool = Field(description="Whether the case is reportable", default=None)
    evidence: list = Field(
        description="The evidence presented in the case", default=None
    )
    conclusion: str = Field(description="The conclusion of the case", default=None)
    courts_reasoning: str = Field(
        description="The court's reasoning in the case", default=None
    )
    precedent_analysis: str = Field(
        description="The analysis of precedents", default=None
    )
    legal_analysis: str = Field(
        description="The legal analysis of the case", default=None
    )
    respondents_arguments: str = Field(
        description="The arguments of the respondent", default=None
    )
    petitioners_arguments: str = Field(
        description="The arguments of the petitioner", default=None
    )
    issues: str = Field(description="The issues addressed in the case", default=None)
    facts: str = Field(description="The facts of the case", default=None)
    summary: str = Field(description="The summary of the case", default=None)
    citations: list = Field(
        description="The citations or case no/names related to the case", default=None
    )
    cited: list = Field(
        description="Other cases cited in this case, that case name/no", default=None
    )
    headnotes: str = Field(description="Headnotes of the case", default=None)
    case_referred: list = Field(
        description="Other cases referred in this case", default=None
    )
    keywords: list = Field(description="Keywords describing the case", default=None)


# Template for asking the LLM to extract information
prompt_template = """
You are tasked with extracting legal case information from the document below. Extract the following fields:
- case_name: (must required)
- case_no: (must required)
- result: 
- overruled: (Yes or No)
- overruled_by: 
- court_name: 
- court_abbreviation:
- case_type: 
- petitioner: 
- respondent: 
- coram: 
- petitioner_counsel: []
- respondent_counsel: []
- act: []
- bench: []
- dated: (must required)
- reportable: 
- evidence: []
- conclusion: 
- courts_reasoning: 
- precedent_analysis: 
- legal_analysis: 
- respondents_arguments: 
- petitioners_arguments: 
- issues: 
- facts: 
- summary: (should point out all key aspects of the case)
- citations: []
- cited: []
- headnotes: 
- case_referred: []
- keywords:[]

If a field is not found, return null for that field except case name, case no, dated. you must find case no and case year for dated and case name.
Document:
{document_text}
"""

def htm_to_json(html_document):
    # Define the JSON output parser based on the CaseInfo model
    parser = JsonOutputParser(pydantic_object=CaseInfo)

    # Create a prompt template
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["document_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # Initialize the LLM
    llm = GoogleGenerativeAI(
        model="models/gemini-1.5-flash-latest", google_api_key=google_api_key
    )

    # Create the LLM chain
    chain = prompt | llm | parser

    response = chain.invoke({"document_text": html_document})
    print('converted into json successfully')
    print(response)

    if response['case_no'] is None:
        response['case_no'] = response['case_name']

    return response
