"""
Root Orchestrator Agent for CodeForge.

This is the main entry point that ADK discovers via `adk web`.
It defines the orchestrator agent with all sub-agents registered as AgentTools.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .prompts import ORCHESTRATOR_PROMPT

# Import all sub-agents
from .sub_agents.requirements_parser import requirements_parser_agent
from .sub_agents.clarification import clarification_agent
from .sub_agents.risk_assessment import risk_assessment_agent
from .sub_agents.availability_analysis import availability_analysis_agent
from .sub_agents.compliance_checker import compliance_checker_agent
from .sub_agents.architecture_designer import architecture_designer_agent
from .sub_agents.code_generator import code_generator_agent
from .sub_agents.code_reviewer import code_reviewer_agent
from .sub_agents.code_executor import code_executor_agent

# Import direct tools for the orchestrator
from .tools._state_tools import update_workflow_state, get_workflow_state
from .tools._rendering_tools import generate_diagram_from_mermaid

# The main Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-pro",
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        # Direct tools
        update_workflow_state,
        get_workflow_state,
        generate_diagram_from_mermaid,
        # Sub-agents wrapped as AgentTools
        AgentTool(requirements_parser_agent),
        AgentTool(clarification_agent),
        AgentTool(risk_assessment_agent),
        AgentTool(availability_analysis_agent),
        AgentTool(compliance_checker_agent),
        AgentTool(architecture_designer_agent),
        AgentTool(code_generator_agent),
        AgentTool(code_reviewer_agent),
        AgentTool(code_executor_agent),
    ],
)

# ADK discovers this as the entry point
root_agent = orchestrator_agent
