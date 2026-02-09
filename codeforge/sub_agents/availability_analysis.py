"""Availability Analysis Agent - Determines availability tiers and resilience patterns."""

from google.adk.agents import LlmAgent
from ..prompts import AVAILABILITY_ANALYSIS_PROMPT

availability_analysis_agent = LlmAgent(
    name="availability_analysis_agent",
    model="gemini-2.5-flash",
    instruction=AVAILABILITY_ANALYSIS_PROMPT,
    output_key="availability_results",
)
