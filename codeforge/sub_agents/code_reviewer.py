"""Code Reviewer Agent - Reviews generated code for quality and security."""

from google.adk.agents import LlmAgent
from ..prompts import CODE_REVIEWER_PROMPT

code_reviewer_agent = LlmAgent(
    name="code_reviewer_agent",
    model="gemini-2.5-flash",
    instruction=CODE_REVIEWER_PROMPT,
)
