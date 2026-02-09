# CodeForge - Requirements to Code Multi-Agent System

A multi-agent POC built with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) that transforms requirement documents into working code, with built-in risk analysis for banking clients.

## Architecture

```
Orchestrator (gemini-2.5-pro)
├── Requirements Parser (gemini-2.5-flash)
├── Clarification Agent (gemini-2.5-flash)
├── Risk Assessment Agent (gemini-2.5-pro)
├── Availability Analysis Agent (gemini-2.5-flash)
├── Compliance Checker Agent (gemini-2.5-pro)
├── Architecture Designer (gemini-2.5-pro)
├── Code Generator (gemini-2.5-pro)
├── Code Reviewer (gemini-2.5-flash)
└── Code Executor (gemini-2.5-flash)
```

## Quick Start on GCP (Cloud Shell or VM)

### 1. Clone and setup

```bash
git clone https://github.com/<your-username>/codeforge.git
cd codeforge
```

### 2. Install Python 3.11+ and dependencies

```bash
# On Debian/Ubuntu VM:
sudo apt update && sudo apt install -y python3.11 python3.11-venv python3-pip

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install google-adk google-cloud-storage pypdf pydantic python-dotenv httpx requests
```

### 3. Configure GCP

```bash
# Copy and edit environment file
cp .env.example .env

# Set your project ID (replace with your actual project)
sed -i 's/your-gcp-project-id/YOUR_PROJECT_ID/' .env
sed -i 's/codeforge-artifacts-your-project-id/codeforge-artifacts-YOUR_PROJECT_ID/' .env

# Authenticate (Cloud Shell is already authenticated)
gcloud auth application-default login

# Run GCP setup (enables APIs, creates bucket)
chmod +x setup_environment.sh
bash setup_environment.sh
```

### 4. Run the dry-run validation

```bash
python3 dry_run.py
```

### 5. Launch ADK Web UI

```bash
# From the codeforge/ directory (the one containing the codeforge/ package)
adk web --port 8080
```

Then open the Web Preview (Cloud Shell) or navigate to `http://<VM_IP>:8080`.
Select **codeforge** from the agent dropdown.

### 6. Try it out

Paste a requirements document or type:
```
Please analyze the requirements in gs://YOUR_BUCKET/requirements/banking_payment_api.md
```

## Project Structure

```
codeforge/                    # Root (run adk web from here)
├── codeforge/                # ADK agent package
│   ├── __init__.py           # Exports root_agent
│   ├── agent.py              # Orchestrator agent definition
│   ├── prompts.py            # All agent prompts
│   ├── sub_agents/           # 9 specialized agents
│   │   ├── requirements_parser.py
│   │   ├── clarification.py
│   │   ├── risk_assessment.py
│   │   ├── availability_analysis.py
│   │   ├── compliance_checker.py
│   │   ├── architecture_designer.py
│   │   ├── code_generator.py
│   │   ├── code_reviewer.py
│   │   └── code_executor.py
│   └── tools/                # Custom tools
│       ├── _state_tools.py
│       ├── _document_tools.py
│       ├── _rendering_tools.py
│       └── _execution_tools.py
├── data/                     # Sample documents
├── dry_run.py                # Validation script
├── setup_environment.sh      # GCP setup
├── .env.example              # Config template
└── pyproject.toml            # Dependencies
```

## Workflow

1. **Upload** requirement document (or paste text)
2. **Parse** → Agent extracts and classifies requirements
3. **Clarify** → Agent asks clarifying questions if ambiguous
4. **Risk Analysis** → Banking risk, compliance, availability checks (advisory)
5. **Design** → Architecture with Mermaid diagrams
6. **Generate** → Complete runnable code
7. **Review** → Automated code quality check
8. **Execute** → Run generated code in sandbox

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Google ADK 1.x |
| LLM | Gemini 2.5 Flash + Pro |
| Cloud | GCP (Vertex AI, Cloud Storage) |
| Language | Python 3.11+ |
