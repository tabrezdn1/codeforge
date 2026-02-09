"""Requirements Parser Agent - Extracts and analyzes requirements from documents."""

from google.adk.agents import LlmAgent
from ..prompts import REQUIREMENTS_PARSER_PROMPT
from ..tools._document_tools import read_document_from_gcs

requirements_parser_agent = LlmAgent(
    name="requirements_parser_agent",
    model="gemini-2.5-flash",
    instruction=REQUIREMENTS_PARSER_PROMPT,
    tools=[read_document_from_gcs],
    output_key="parsed_requirements",
)
