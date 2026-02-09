"""Compliance Checker Agent - Validates against SOX, PCI-DSS, GDPR, Basel III."""

from google.adk.agents import LlmAgent
from ..prompts import COMPLIANCE_CHECKER_PROMPT

compliance_checker_agent = LlmAgent(
    name="compliance_checker_agent",
    model="gemini-2.5-flash",
    instruction=COMPLIANCE_CHECKER_PROMPT,
    output_key="compliance_results",
)
