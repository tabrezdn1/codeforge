"""Code Generator Agent - Generates complete, runnable project code."""

from google.adk.agents import LlmAgent
from ..prompts import CODE_GENERATOR_PROMPT

code_generator_agent = LlmAgent(
    name="code_generator_agent",
    model="gemini-2.5-flash",
    instruction=CODE_GENERATOR_PROMPT,
)
