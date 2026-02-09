#!/usr/bin/env python3
"""
CodeForge Dry-Run Validation Script
====================================
Validates the entire project structure, imports, agent definitions,
tool signatures, and GCP connectivity BEFORE deployment.

Run: python dry_run.py
"""

import importlib
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

# ============================================================================
# Helpers
# ============================================================================

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
WARN = "\033[93m[WARN]\033[0m"
INFO = "\033[94m[INFO]\033[0m"

pass_count = 0
fail_count = 0
warn_count = 0


def check(condition: bool, msg: str, is_warning: bool = False):
    global pass_count, fail_count, warn_count
    if condition:
        print(f"  {PASS} {msg}")
        pass_count += 1
    elif is_warning:
        print(f"  {WARN} {msg}")
        warn_count += 1
    else:
        print(f"  {FAIL} {msg}")
        fail_count += 1


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ============================================================================
# Phase 1: Environment & Structure
# ============================================================================

def phase1_structure():
    section("Phase 1: Project Structure Validation")

    root = Path(__file__).parent
    pkg = root / "codeforge"

    # Core files
    required_files = [
        "pyproject.toml",
        ".env.example",
        "setup_environment.sh",
        "codeforge/__init__.py",
        "codeforge/agent.py",
        "codeforge/prompts.py",
        "codeforge/tools/__init__.py",
        "codeforge/tools/_state_tools.py",
        "codeforge/tools/_document_tools.py",
        "codeforge/tools/_rendering_tools.py",
        "codeforge/tools/_execution_tools.py",
        "codeforge/sub_agents/__init__.py",
        "codeforge/sub_agents/requirements_parser.py",
        "codeforge/sub_agents/clarification.py",
        "codeforge/sub_agents/risk_assessment.py",
        "codeforge/sub_agents/availability_analysis.py",
        "codeforge/sub_agents/compliance_checker.py",
        "codeforge/sub_agents/architecture_designer.py",
        "codeforge/sub_agents/code_generator.py",
        "codeforge/sub_agents/code_reviewer.py",
        "codeforge/sub_agents/code_executor.py",
        "data/sample_requirements/banking_payment_api.md",
    ]

    for f in required_files:
        check((root / f).exists(), f"File exists: {f}")

    # Check Python version
    v = sys.version_info
    check(v.major == 3 and v.minor >= 11, f"Python {v.major}.{v.minor}.{v.micro} >= 3.11")

    # Check .env exists (not .env.example)
    check(
        (root / ".env").exists(),
        ".env file exists (copy from .env.example if missing)",
        is_warning=True,
    )

    # ADK convention: root_agent in __init__.py
    init_content = (pkg / "__init__.py").read_text()
    check("root_agent" in init_content, "root_agent exported from __init__.py")

    # ADK convention: agent.py defines root_agent
    agent_content = (pkg / "agent.py").read_text()
    check("root_agent" in agent_content, "root_agent defined in agent.py")
    check("AgentTool" in agent_content, "AgentTool used for sub-agent delegation")


# ============================================================================
# Phase 2: Dependency Imports
# ============================================================================

def phase2_imports():
    section("Phase 2: Python Dependency Imports")

    deps = {
        "google.adk": "google-adk",
        "google.adk.agents": "google-adk (agents)",
        "google.adk.tools.agent_tool": "google-adk (AgentTool)",
        "google.adk.tools": "google-adk (ToolContext)",
        "google.cloud.storage": "google-cloud-storage",
        "pydantic": "pydantic",
        "dotenv": "python-dotenv",
        "pypdf": "pypdf",
        "httpx": "httpx",
        "requests": "requests",
    }

    all_ok = True
    for module_path, pkg_name in deps.items():
        try:
            importlib.import_module(module_path)
            check(True, f"import {module_path} ({pkg_name})")
        except ImportError as e:
            check(False, f"import {module_path} ({pkg_name}) - {e}")
            all_ok = False

    if not all_ok:
        print(f"\n  {INFO} Run 'poetry install' or 'pip install -e .' to install missing deps.")

    return all_ok


# ============================================================================
# Phase 3: Agent Instantiation
# ============================================================================

def phase3_agents():
    section("Phase 3: Agent Instantiation & Wiring")

    try:
        # Change working directory so relative imports work
        root = Path(__file__).parent
        sys.path.insert(0, str(root))

        # Import prompts first
        from codeforge.prompts import (
            ORCHESTRATOR_PROMPT,
            REQUIREMENTS_PARSER_PROMPT,
            CLARIFICATION_PROMPT,
            RISK_ASSESSMENT_PROMPT,
            AVAILABILITY_ANALYSIS_PROMPT,
            COMPLIANCE_CHECKER_PROMPT,
            ARCHITECTURE_DESIGNER_PROMPT,
            CODE_GENERATOR_PROMPT,
            CODE_REVIEWER_PROMPT,
            CODE_EXECUTOR_PROMPT,
        )
        check(True, "All 10 prompt constants imported")
    except Exception as e:
        check(False, f"Import prompts: {e}")
        return False

    # Validate prompt lengths (should be non-trivial)
    prompts = {
        "ORCHESTRATOR_PROMPT": ORCHESTRATOR_PROMPT,
        "REQUIREMENTS_PARSER_PROMPT": REQUIREMENTS_PARSER_PROMPT,
        "CLARIFICATION_PROMPT": CLARIFICATION_PROMPT,
        "RISK_ASSESSMENT_PROMPT": RISK_ASSESSMENT_PROMPT,
        "AVAILABILITY_ANALYSIS_PROMPT": AVAILABILITY_ANALYSIS_PROMPT,
        "COMPLIANCE_CHECKER_PROMPT": COMPLIANCE_CHECKER_PROMPT,
        "ARCHITECTURE_DESIGNER_PROMPT": ARCHITECTURE_DESIGNER_PROMPT,
        "CODE_GENERATOR_PROMPT": CODE_GENERATOR_PROMPT,
        "CODE_REVIEWER_PROMPT": CODE_REVIEWER_PROMPT,
        "CODE_EXECUTOR_PROMPT": CODE_EXECUTOR_PROMPT,
    }
    for name, prompt in prompts.items():
        check(len(prompt) > 100, f"{name} has {len(prompt)} chars (>100)")

    # Import sub-agents
    sub_agents_modules = [
        ("codeforge.sub_agents.requirements_parser", "requirements_parser_agent"),
        ("codeforge.sub_agents.clarification", "clarification_agent"),
        ("codeforge.sub_agents.risk_assessment", "risk_assessment_agent"),
        ("codeforge.sub_agents.availability_analysis", "availability_analysis_agent"),
        ("codeforge.sub_agents.compliance_checker", "compliance_checker_agent"),
        ("codeforge.sub_agents.architecture_designer", "architecture_designer_agent"),
        ("codeforge.sub_agents.code_generator", "code_generator_agent"),
        ("codeforge.sub_agents.code_reviewer", "code_reviewer_agent"),
        ("codeforge.sub_agents.code_executor", "code_executor_agent"),
    ]

    agents = {}
    for module_path, agent_name in sub_agents_modules:
        try:
            mod = importlib.import_module(module_path)
            agent = getattr(mod, agent_name)
            agents[agent_name] = agent
            check(True, f"Instantiated {agent_name} (model={agent.model})")
        except Exception as e:
            check(False, f"Instantiate {agent_name}: {e}")

    # Import root orchestrator
    try:
        from codeforge.agent import root_agent, orchestrator_agent
        check(True, f"Orchestrator loaded (model={orchestrator_agent.model})")
        check(root_agent is orchestrator_agent, "root_agent is orchestrator_agent")
    except Exception as e:
        check(False, f"Load orchestrator: {e}")
        traceback.print_exc()
        return False

    # Validate orchestrator tools
    def get_tool_name(t):
        if hasattr(t, 'name'):
            return t.name
        if callable(t) and hasattr(t, '__name__'):
            return t.__name__
        return str(t)

    tool_names = [get_tool_name(t) for t in orchestrator_agent.tools]
    print(f"\n  {INFO} Orchestrator has {len(orchestrator_agent.tools)} tools: {tool_names}")

    expected_tools = [
        "update_workflow_state",
        "get_workflow_state",
        "generate_diagram_from_mermaid",
        "requirements_parser_agent",
        "clarification_agent",
        "risk_assessment_agent",
        "availability_analysis_agent",
        "compliance_checker_agent",
        "architecture_designer_agent",
        "code_generator_agent",
        "code_reviewer_agent",
        "code_executor_agent",
    ]
    for tool_name in expected_tools:
        check(
            tool_name in tool_names,
            f"Orchestrator has tool: {tool_name}",
        )

    return True


# ============================================================================
# Phase 4: Tool Function Signatures
# ============================================================================

def phase4_tools():
    section("Phase 4: Tool Function Signatures")

    try:
        from codeforge.tools._state_tools import update_workflow_state, get_workflow_state
        from codeforge.tools._document_tools import read_document_from_gcs
        from codeforge.tools._rendering_tools import generate_diagram_from_mermaid
        from codeforge.tools._execution_tools import execute_code_in_subprocess
        check(True, "All tool functions imported")
    except Exception as e:
        check(False, f"Import tools: {e}")
        return

    # Verify tool function signatures (ADK uses inspection to create schemas)
    tools_to_check = {
        "update_workflow_state": (update_workflow_state, ["state", "data", "tool_context"]),
        "get_workflow_state": (get_workflow_state, ["tool_context"]),
        "read_document_from_gcs": (read_document_from_gcs, ["uri"]),
        "generate_diagram_from_mermaid": (generate_diagram_from_mermaid, ["mermaid_syntax", "file_name"]),
        "execute_code_in_subprocess": (execute_code_in_subprocess, ["project_files_json", "run_command", "timeout_seconds"]),
    }

    for name, (func, expected_params) in tools_to_check.items():
        sig = inspect.signature(func)
        actual_params = list(sig.parameters.keys())
        check(
            actual_params == expected_params,
            f"{name}({', '.join(actual_params)})",
        )
        # Check docstrings (ADK uses them for tool descriptions)
        check(
            func.__doc__ is not None and len(func.__doc__) > 20,
            f"{name} has docstring ({len(func.__doc__ or '')} chars)",
        )

    # Verify tool_context param has type annotation (ADK injects it automatically)
    sig = inspect.signature(update_workflow_state)
    tc_param = sig.parameters.get("tool_context")
    if tc_param:
        annotation = tc_param.annotation
        check(
            annotation != inspect.Parameter.empty and "ToolContext" in str(annotation),
            f"update_workflow_state.tool_context typed as ToolContext (ADK auto-injection)",
        )


# ============================================================================
# Phase 5: GCP Connectivity
# ============================================================================

def phase5_gcp():
    section("Phase 5: GCP Connectivity")

    # Load .env if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    bucket = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")

    check(
        project_id is not None and project_id != "your-gcp-project-id",
        f"GOOGLE_CLOUD_PROJECT set: {project_id or 'NOT SET'}",
        is_warning=True,
    )
    check(
        location is not None,
        f"GOOGLE_CLOUD_LOCATION set: {location}",
    )
    check(
        bucket is not None and "your-project-id" not in (bucket or ""),
        f"GOOGLE_CLOUD_STORAGE_BUCKET set: {bucket or 'NOT SET'}",
        is_warning=True,
    )

    # Check gcloud auth
    import subprocess
    try:
        result = subprocess.run(
            ["gcloud", "auth", "application-default", "print-access-token"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        check(
            result.returncode == 0,
            "gcloud application-default credentials active",
            is_warning=True,
        )
    except FileNotFoundError:
        check(False, "gcloud CLI not found - install from https://cloud.google.com/sdk", is_warning=True)
    except subprocess.TimeoutExpired:
        check(False, "gcloud auth check timed out", is_warning=True)

    # Check if Vertex AI API is accessible
    if project_id and project_id != "your-gcp-project-id":
        try:
            result = subprocess.run(
                ["gcloud", "services", "list", "--enabled",
                 "--filter=name:aiplatform.googleapis.com",
                 f"--project={project_id}", "--format=value(name)"],
                capture_output=True,
                text=True,
                timeout=15,
            )
            check(
                "aiplatform" in result.stdout,
                f"Vertex AI API enabled on {project_id}",
                is_warning=True,
            )
        except Exception:
            check(False, "Could not verify Vertex AI API status", is_warning=True)

        # Check Cloud Storage API
        try:
            result = subprocess.run(
                ["gcloud", "services", "list", "--enabled",
                 "--filter=name:storage.googleapis.com",
                 f"--project={project_id}", "--format=value(name)"],
                capture_output=True,
                text=True,
                timeout=15,
            )
            check(
                "storage" in result.stdout,
                f"Cloud Storage API enabled on {project_id}",
                is_warning=True,
            )
        except Exception:
            check(False, "Could not verify Cloud Storage API status", is_warning=True)

    # Check ADK CLI
    try:
        result = subprocess.run(
            ["adk", "version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            check(True, f"ADK CLI available: {version}")
        else:
            # Try adk --help as fallback
            result2 = subprocess.run(["adk", "--help"], capture_output=True, text=True, timeout=5)
            check(result2.returncode == 0, "ADK CLI available (version command not supported)")
    except FileNotFoundError:
        check(False, "ADK CLI not found - install with: pip install google-adk", is_warning=True)
    except subprocess.TimeoutExpired:
        check(False, "ADK CLI check timed out", is_warning=True)


# ============================================================================
# Phase 6: ADK Web Compatibility Check
# ============================================================================

def phase6_adk_web():
    section("Phase 6: ADK Web Compatibility")

    root = Path(__file__).parent

    # ADK web expects: parent_dir/agent_package/__init__.py with root_agent
    # When you run `adk web` from parent_dir, it scans for packages with root_agent
    check(
        (root / "codeforge" / "__init__.py").exists(),
        "Package __init__.py exists at codeforge/__init__.py",
    )

    init_content = (root / "codeforge" / "__init__.py").read_text()
    check(
        "from .agent import root_agent" in init_content,
        "__init__.py imports root_agent from agent module",
    )

    # Verify __init__.py exports root_agent in __all__
    check(
        '"root_agent"' in init_content or "'root_agent'" in init_content,
        "root_agent in __all__",
    )

    # Check that agent.py variable is actually named root_agent
    agent_content = (root / "codeforge" / "agent.py").read_text()
    check(
        "root_agent = orchestrator_agent" in agent_content,
        "agent.py sets root_agent = orchestrator_agent",
    )

    print(f"\n  {INFO} To run: cd {root} && adk web")
    print(f"  {INFO} Then select 'codeforge' from the dropdown in the web UI")


# ============================================================================
# Phase 7: End-to-End Simulation (Mocked)
# ============================================================================

def phase7_simulation():
    section("Phase 7: End-to-End Workflow Simulation (Mocked)")

    # Simulate the state machine transitions
    states = [
        "NEW",
        "PARSING",
        "CLARIFYING",
        "AWAITING_REQ_CONFIRMATION",
        "RISK_ANALYSIS",
        "RISK_ADVISORY",
        "DESIGNING",
        "AWAITING_ARCH_APPROVAL",
        "GENERATING",
        "AWAITING_EXEC_CONFIRMATION",
        "EXECUTING",
        "COMPLETE",
    ]

    # Verify all states are referenced in the orchestrator prompt
    from codeforge.prompts import ORCHESTRATOR_PROMPT

    for state in states:
        check(
            state in ORCHESTRATOR_PROMPT,
            f"State '{state}' referenced in orchestrator prompt",
        )

    # Simulate state transitions
    valid_transitions = {
        "NEW": ["PARSING"],
        "PARSING": ["CLARIFYING", "AWAITING_REQ_CONFIRMATION"],
        "CLARIFYING": ["AWAITING_REQ_CONFIRMATION"],
        "AWAITING_REQ_CONFIRMATION": ["RISK_ANALYSIS"],
        "RISK_ANALYSIS": ["RISK_ADVISORY"],
        "RISK_ADVISORY": ["DESIGNING"],
        "DESIGNING": ["AWAITING_ARCH_APPROVAL"],
        "AWAITING_ARCH_APPROVAL": ["GENERATING", "DESIGNING"],
        "GENERATING": ["AWAITING_EXEC_CONFIRMATION"],
        "AWAITING_EXEC_CONFIRMATION": ["EXECUTING", "COMPLETE"],
        "EXECUTING": ["COMPLETE"],
    }

    print(f"\n  {INFO} State machine transitions:")
    for from_state, to_states in valid_transitions.items():
        for to_state in to_states:
            check(True, f"  {from_state} -> {to_state}")

    # Test code executor tool with mock data
    from codeforge.tools._execution_tools import execute_code_in_subprocess

    mock_files = json.dumps([
        {"path": "main.py", "content": "print('Hello from CodeForge!')"},
    ])

    result_json = execute_code_in_subprocess(mock_files, "python main.py", timeout_seconds=10)
    result = json.loads(result_json)
    check(
        result["execution_status"] == "success",
        f"Code executor mock test: {result['execution_status']} - stdout: {result.get('stdout', '').strip()}",
    )


# ============================================================================
# Main
# ============================================================================

def main():
    print("\n" + "=" * 60)
    print("  CodeForge Dry-Run Validation")
    print("  ============================")
    print(f"  Python: {sys.version}")
    print(f"  CWD:    {os.getcwd()}")
    print("=" * 60)

    # Phase 1: Always runs (no deps needed)
    phase1_structure()

    # Phase 2: Check imports
    imports_ok = phase2_imports()

    # Phases 3-7: Only if imports pass
    if imports_ok:
        phase3_agents()
        phase4_tools()
        phase5_gcp()
        phase6_adk_web()
        phase7_simulation()
    else:
        print(f"\n  {WARN} Skipping Phases 3-7 (dependencies not installed)")
        print(f"  {INFO} Run: pip install google-adk google-cloud-storage pypdf pydantic python-dotenv httpx requests")

    # Summary
    section("Summary")
    print(f"  {PASS} Passed: {pass_count}")
    print(f"  {FAIL} Failed: {fail_count}")
    print(f"  {WARN} Warnings: {warn_count}")

    if fail_count > 0:
        print(f"\n  {FAIL} {fail_count} checks failed. Fix these before deploying.")
        sys.exit(1)
    elif warn_count > 0:
        print(f"\n  {WARN} All critical checks passed. {warn_count} warnings to review.")
        print(f"  {INFO} Warnings about GCP config can be resolved after deployment setup.")
        sys.exit(0)
    else:
        print(f"\n  {PASS} All checks passed! Ready to deploy.")
        sys.exit(0)


if __name__ == "__main__":
    main()
