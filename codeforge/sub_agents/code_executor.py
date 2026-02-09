"""Code Executor Agent - Executes generated code in subprocess sandbox."""

from google.adk.agents import LlmAgent
from ..prompts import CODE_EXECUTOR_PROMPT
from ..tools._execution_tools import execute_code_in_subprocess

code_executor_agent = LlmAgent(
    name="code_executor_agent",
    model="gemini-2.5-flash",
    instruction=CODE_EXECUTOR_PROMPT,
    tools=[execute_code_in_subprocess],
)
