# Requirements-to-Code Multi-Agent System
## Executive Summary

**Version:** 1.1 | **Status:** Draft | **Date:** February 4, 2026  
**Target Client:** Banking / Financial Services

---

## What Is This?

A **multi-agent AI system** that transforms requirement documents into working, executable code. Think of it as an AI development team where each "team member" (agent) has a specialized role.

**Banking-Specific Features:**
- Risk Analysis (Operational, Security, Availability)
- Regulatory Compliance Checks (SOX, PCI-DSS, GDPR, Basel III)
- High Availability Architecture Patterns (99.99% uptime)
- Resilience Patterns (Circuit Breakers, Retry, Graceful Degradation)

---

## The Problem

Converting requirements to code involves multiple complex steps:

1. Understanding what the requirements actually mean
2. Asking clarifying questions when things are unclear
3. Designing an appropriate architecture
4. Writing correct, complete code
5. Making sure the code actually runs

**A single AI prompt can't reliably do all of this.** The context is too large, and different tasks need different approaches.

---

## The Solution: Specialized Agents

```
┌─────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR                              │
│                    (Traffic Controller)                          │
└─────────────────────────────────────────────────────────────────┘
         │           │           │           │           │
         ▼           ▼           ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Parser  │ │Clarifier│ │Architect│ │  Coder  │ │Executor │
    │  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │
    └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
    "What do    "What's     "How to    "Write the  "Run and
     they       unclear?"    build it?" code"       test it"
     want?"
```

### The Agents

| Agent | Role | Analogy |
|-------|------|---------|
| **Orchestrator** | Coordinates workflow, manages state | Project Manager |
| **Requirements Parser** | Extracts requirements from documents | Business Analyst |
| **Clarification Agent** | Asks questions about ambiguities | QA Analyst |
| **Risk Assessment Agent** | Analyzes operational, security, availability risks | Risk Officer ⭐ |
| **Availability Analysis Agent** | Determines uptime tiers and resilience needs | SRE Lead ⭐ |
| **Compliance Checker Agent** | Validates against SOX, PCI-DSS, GDPR | Compliance Officer ⭐ |
| **Architecture Designer** | Designs system structure | Solutions Architect |
| **Code Generator** | Writes the actual code | Developer |
| **Code Reviewer** | Checks code quality | Senior Developer |
| **Code Executor** | Runs code in sandbox | DevOps Engineer |

⭐ Banking-specific agents

---

## The Workflow

```
[Document] → Parse → Clarify → Confirm → Risk Analysis → Design → Approve → Generate → Review → Execute
                ↑        │                    ↓                      ↑          │
                └────────┘              (advisory report)            └──────────┘
              (ask questions)            [does NOT block]          (fix issues)
```

### Key User Checkpoints

The system **always stops and asks** before:

1. **After parsing** → "Here are the requirements I found. Proceed?"
2. **After risk analysis** → "Here's the risk advisory report." (advisory only - doesn't block) ⭐
3. **After architecture** → "Here's my design [diagram]. Approve?"
4. **Before execution** → "Code is ready. Run it?"

⭐ **Banking Feature:** Risk analysis runs automatically after requirements confirmation. It generates an advisory report covering:
- Operational risks
- Security risks  
- Availability requirements
- Compliance gaps (SOX, PCI-DSS, GDPR)

The workflow continues after you acknowledge the report - it's advisory, not blocking.

---

## Technology Choices

| What | Technology | Why |
|------|------------|-----|
| Multi-Agent Framework | **Google ADK** | Google's official agent toolkit |
| AI Model | **Gemini 2.0** | Required: Google ecosystem |
| Cloud Storage | **Google Cloud Storage** | Documents and artifacts |
| Code Execution | **Docker** | Safe, isolated sandboxes |

---

## Sample Interaction

**User uploads:** `requirements.pdf`

**System:**
> "I've parsed your document and found 8 requirements. 2 have ambiguities:
> 
> 1. 'Secure authentication' - What method? (JWT / OAuth2 / Session)
> 2. 'Handle many users' - What's the target number?"

**User:** "Use JWT. Target 100 concurrent users."

**System:**
> "Requirements clarified. Ready to design architecture. Proceed?"

**User:** "Yes"

**System:**
> "Here's the proposed architecture:
> 
> [Shows diagram]
> 
> - Pattern: Layered API
> - Stack: Python, FastAPI, SQLite, JWT
> 
> Shall I generate the code?"

**User:** "Yes"

**System:**
> "Generated 6 files. Code review passed. Ready to execute?"

**User:** "Yes"

**System:**
> "Execution successful! API running. Test results: 5/5 passed.
> Here's your project: [download link]"

---

## What Makes This Different?

| Traditional Approach | This System |
|---------------------|-------------|
| Single prompt, hope for the best | Specialized agents for each task |
| No clarification | Asks questions when unclear |
| Code snippets | Complete, runnable projects |
| Manual testing | Automated execution in sandbox |
| Black box | Visual architecture approval |

---

## Implementation Phases

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Foundation | 1 week | Basic orchestrator + parser |
| 2. Clarification | 1 week | Question/answer loop |
| 3. Architecture | 1 week | Design + diagrams |
| 4. Code Generation | 1-2 weeks | Complete code output |
| 5. Execution | 1 week | Docker sandbox |
| 6. Polish | 1 week | Error handling, docs |

**Total: ~6 weeks for full POC**

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Generated code has bugs | High | Code reviewer agent + sandbox testing |
| Sandbox security issues | High | Docker isolation, resource limits |
| LLM generates incorrect architecture | Medium | Human approval gate |
| Complex requirements overwhelm system | Medium | Scope to single-service apps |

---

## Next Steps

1. **Review this document** - Does the approach make sense?
2. **Approve architecture** - Sign off on the design
3. **Begin implementation** - Start with Phase 1

---

## Questions?

Key decisions that need input:

1. **Scope:** Should POC support only Python, or multiple languages?
2. **Execution:** Docker locally vs Cloud Run for sandboxes?
3. **Storage:** Ephemeral (in-memory) vs persistent (GCS) for sessions?

---

## Key Implementation Details

The full architecture document now includes a comprehensive **Section 5: Implementation Deep Dive** that covers:

- **5.1 Document Processing Pipeline** - How documents are ingested, parsed (PDF/MD/TXT), and chunked
- **5.2 Embedding & Vector Storage** - Using `text-embedding-004` (768-dim) with Vertex AI
- **5.3 RAG Architecture** - Vertex AI RAG Corpus setup and BigQuery vector search
- **5.4 Requirement Analysis & Decision Logic** - How ambiguity is scored and detected
- **5.5 Clarification Decision Flow** - When clarification is required vs optional vs not needed
- **5.6 End-to-End Processing Flow** - Complete 12-phase workflow with state transitions
- **5.7 Risk Analysis & Compliance** ⭐ - Banking risk scoring, compliance framework checks
- **5.8 Availability & Resilience** ⭐ - Availability tiers, resilience patterns, SLA requirements

⭐ **Banking-specific sections** added for financial services requirements.

This follows patterns from [Project Agora](https://github.com/MohitBhimrajka/project-agora), Google's reference implementation for ADK multi-agent systems.

---

*Full technical details: See [ARCHITECTURE.md](./ARCHITECTURE.md)*
