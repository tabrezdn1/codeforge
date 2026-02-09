"""State management tools for CodeForge."""

import json
from google.adk.tools import ToolContext


def update_workflow_state(state: str, data: str, tool_context: ToolContext) -> str:
    """
    Updates the workflow state in the session.

    Args:
        state: The new workflow state (e.g., NEW, PARSING, CLARIFYING, etc.)
        data: JSON string of additional data to store with the state.
        tool_context: ADK tool context for session state access.

    Returns:
        Confirmation message.
    """
    tool_context.state["workflow_state"] = state

    if data:
        try:
            parsed_data = json.loads(data) if isinstance(data, str) else data
            tool_context.state["workflow_data"] = json.dumps(parsed_data)
        except (json.JSONDecodeError, TypeError):
            tool_context.state["workflow_data"] = data

    return f"Workflow state updated to: {state}"


def get_workflow_state(tool_context: ToolContext) -> str:
    """
    Retrieves the current workflow state from the session.

    Args:
        tool_context: ADK tool context for session state access.

    Returns:
        JSON string with current state and data.
    """
    current_state = tool_context.state.get("workflow_state", "NONE")
    current_data = tool_context.state.get("workflow_data", "{}")

    return json.dumps({
        "state": current_state,
        "data": current_data,
    })
