"""Risk Assessment Agent - Analyzes operational, security, and availability risks."""

from google.adk.agents import LlmAgent
from ..prompts import RISK_ASSESSMENT_PROMPT

risk_assessment_agent = LlmAgent(
    name="risk_assessment_agent",
    model="gemini-2.5-flash",
    instruction=RISK_ASSESSMENT_PROMPT,
    output_key="risk_assessment_results",
)
