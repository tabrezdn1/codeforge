"""Code execution tools for CodeForge (POC - subprocess-based)."""

import json
import os
import subprocess
import tempfile


def execute_code_in_subprocess(project_files_json: str, run_command: str, timeout_seconds: int = 60) -> str:
    """
    Executes generated code in a temporary directory via subprocess.
    This is the POC implementation - production would use Docker/Cloud Run.

    Args:
        project_files_json: JSON string of files list, each with 'path' and 'content'.
        run_command: The command to run (e.g., 'python src/main.py').
        timeout_seconds: Maximum execution time in seconds.

    Returns:
        JSON string with execution results.
    """
    try:
        files = json.loads(project_files_json) if isinstance(project_files_json, str) else project_files_json
    except json.JSONDecodeError as e:
        return json.dumps({"execution_status": "failure", "error": f"Invalid JSON: {e}"})

    results = {
        "execution_status": "unknown",
        "steps": [],
        "stdout": "",
        "stderr": "",
    }

    with tempfile.TemporaryDirectory(prefix="codeforge_") as tmpdir:
        # Step 1: Write project files
        try:
            for f in files:
                filepath = os.path.join(tmpdir, f["path"])
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w") as fh:
                    fh.write(f["content"])
            results["steps"].append({"step": "write_files", "status": "success"})
        except Exception as e:
            results["execution_status"] = "failure"
            results["steps"].append({"step": "write_files", "status": "failure", "error": str(e)})
            return json.dumps(results)

        # Step 2: Install dependencies (if requirements.txt exists)
        req_file = os.path.join(tmpdir, "requirements.txt")
        if os.path.exists(req_file):
            try:
                pip_result = subprocess.run(
                    ["pip", "install", "-r", req_file, "--quiet"],
                    cwd=tmpdir,
                    timeout=timeout_seconds,
                    capture_output=True,
                    text=True,
                )
                results["steps"].append({
                    "step": "install_dependencies",
                    "status": "success" if pip_result.returncode == 0 else "failure",
                    "output": pip_result.stdout[:500],
                })
            except subprocess.TimeoutExpired:
                results["execution_status"] = "timeout"
                results["steps"].append({"step": "install_dependencies", "status": "timeout"})
                return json.dumps(results)

        # Step 3: Run the code
        try:
            run_result = subprocess.run(
                run_command.split(),
                cwd=tmpdir,
                timeout=timeout_seconds,
                capture_output=True,
                text=True,
            )
            results["stdout"] = run_result.stdout[:2000]
            results["stderr"] = run_result.stderr[:2000]
            results["execution_status"] = "success" if run_result.returncode == 0 else "failure"
            results["steps"].append({
                "step": "run_code",
                "status": "success" if run_result.returncode == 0 else "failure",
                "exit_code": run_result.returncode,
            })
        except subprocess.TimeoutExpired:
            results["execution_status"] = "timeout"
            results["steps"].append({"step": "run_code", "status": "timeout"})
        except Exception as e:
            results["execution_status"] = "failure"
            results["steps"].append({"step": "run_code", "status": "failure", "error": str(e)})

    return json.dumps(results, indent=2)
