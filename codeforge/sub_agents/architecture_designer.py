"""Architecture Designer Agent - Designs system architecture with diagrams."""

from google.adk.agents import LlmAgent
from ..prompts import ARCHITECTURE_DESIGNER_PROMPT
from ..tools._rendering_tools import generate_diagram_from_mermaid

architecture_designer_agent = LlmAgent(
    name="architecture_designer_agent",
    model="gemini-2.5-pro",
    instruction=ARCHITECTURE_DESIGNER_PROMPT,
    tools=[generate_diagram_from_mermaid],
    output_key="architecture_output",
)
