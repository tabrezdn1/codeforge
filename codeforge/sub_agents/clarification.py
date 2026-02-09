"""Clarification Agent - Generates and processes clarifying questions."""

from google.adk.agents import LlmAgent
from ..prompts import CLARIFICATION_PROMPT

clarification_agent = LlmAgent(
    name="clarification_agent",
    model="gemini-2.5-flash",
    instruction=CLARIFICATION_PROMPT,
    output_key="clarification_results",
)
