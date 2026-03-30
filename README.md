# ReguGuard AI

Multi-agent regulatory intelligence system for banks, NBFCs, and fintech teams.

ReguGuard AI automates the compliance workflow for changing RBI regulations: it compares old vs new circulars, decides business applicability, scores risk, and generates an audit-ready report with reasoning from every agent.

## Hackathon Context

This project is built for the challenge: **Domain-Specialized AI Agents with Compliance Guardrails**.

- Domain: Finance / RegTech
- Use case: Regulatory change intelligence and compliance triage
- Objective: End-to-end task completion with edge-case handling and auditable decisions

## Problem Statement

Financial institutions face frequent and complex regulatory updates. Manual legal/compliance review is slow, expensive, and vulnerable to oversight.

- Manual turnaround: ~6 to 8 hours per circular
- Manual cost: high legal/compliance analyst effort
- Risk: missed changes, delayed response, potential penalties

## Solution Overview

ReguGuard AI uses a **5-agent orchestration pipeline** with guardrails to deliver explainable compliance outcomes.

1. Ingestion Agent extracts and structures regulation text from PDFs.
2. Change Detection Agent performs semantic delta analysis between old and new circulars.
3. Compliance Reasoner evaluates applicability to a selected SME/financial profile.
4. Risk Scoring Agent assigns operational/compliance risk (High/Medium/Low).
5. Report Generation Agent produces executive summary plus audit trail.

The orchestrator coordinates each stage and adds cooldown delays to reduce rate-limit failures.

## Why This Is Not Just a Chatbot

- Specialized agents with single responsibilities
- Deterministic orchestration order
- Profile-aware compliance reasoning
- Structured audit trail for each decision
- Graceful fallback behavior on API quota or transient model failures

## Architecture

```text
Regulatory PDFs (old/new)
        |
        v
Ingestion Agent (PyPDF + chunking + embeddings hooks)
        |
        v
Change Detection Agent (semantic deltas)
        |
        v
Compliance Reasoner (applicability guardrail)
        |
        v
Risk Scoring Agent (severity + effort + deadlines)
        |
        v
Report Generation Agent (executive summary + action items)
        |
        v
Streamlit Dashboard (report + audit trail)
```

Detailed design document: `ARCHITECTURE.md`

## Key Guardrails and Edge-Case Handling

- **Applicability guardrail**: recommendations are profile-specific, not generic.
- **Auditability guardrail**: report includes traceable intermediate reasoning.
- **Runtime resilience guardrail**: each LLM-based agent has exception fallback for rate-limit/API issues.
- **Orchestrator cooldown**: explicit delays between model-heavy stages reduce free-tier quota spikes.
- **Data integrity behavior**: the workflow surfaces insufficiencies instead of silently guessing.

## Tech Stack

- Python 3.10+
- Streamlit
- LangChain ecosystem (`langchain`, `langchain-core`, `langchain-google-genai`, `langchain-community`)
- Google Gemini models (`gemini-2.5-flash` in current code)
- Gemini embeddings (`models/embedding-001`)
- FAISS vector store
- Pydantic schema validation
- Loguru logging

## Repository Structure

```text
reguguard_ai/
|-- app.py
|-- test_run.py
|-- ARCHITECTURE.md
|-- IMPACT_MODEL.md
|-- requirements.txt
|-- src/
|   |-- orchestrator.py
|   |-- schema.py
|   |-- agents/
|   |   |-- change_detector.py
|   |   |-- compliance_reasoner.py
|   |   |-- risk_agent.py
|   |   |-- report_agent.py
|   |-- utils/
|       |-- pdf_engine.py
|-- data/
|   |-- profiles/
|   |   |-- commercial_bank_under_threshold.json
|   |   |-- fintech_startup.json
|   |   |-- nbfc_small.json
|   |   |-- private_bank_mid.json
|   |   |-- small_finance_bank_excluded.json
|   |-- raw_pdfs/
```

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and add your key.

```powershell
copy .env.example .env
```

You must set one of these:

```env
GOOGLE_API_KEY=your_google_api_key
# or
GEMINI_API_KEY=your_gemini_api_key
```

## Run the Project

### Streamlit Dashboard (recommended)

```powershell
streamlit run app.py
```

### CLI Smoke Run

```powershell
python test_run.py
```

## Demo Flow (3-Minute Pitch Script Friendly)

1. Select an entity profile from `data/profiles`.
2. Upload old and new regulation PDFs.
3. Click **Run Compliance Audit**.
4. Show the generated output tabs:
   - Executive Summary
   - Audit Trail and Agent Reasoning
   - Action Items
5. Highlight risk classification and profile-specific applicability.

## Data Assets Used

- RBI Internal Ombudsman direction set (old vs new versions)
- RBI prudential/dividend regulation sample
- Multiple JSON entity profiles (commercial bank, NBFC, fintech, small finance bank)

## Quantified Impact Model

- Time: 8 hours manual review to ~45 seconds automated triage
- Cost: approx. $500 manual review to approx. $0.50 to $1.00 token cost
- Risk posture: improved consistency and reduced missed-change probability via structured checks

See `IMPACT_MODEL.md` for assumptions and annualized estimate logic.

## Submission Artifacts Checklist

- Public source code repository: this repo
- Clear setup and run instructions: this README
- Architecture document (1 to 2 pages): `ARCHITECTURE.md`
- Quantified impact model: `IMPACT_MODEL.md`
- 3-minute pitch video: add link here before final submission

```text
Pitch Video URL: https://drive.google.com/file/d/1MtKuR2L3k7abV8LP13RXkyH04cqv38fP/view?usp=sharing
```

## Current Limitations

- Free-tier API quotas can throttle long or repeated runs.
- Some outputs are generated summaries and still require human approval before policy changes.
- Regulatory interpretation remains a decision-support workflow, not legal advice.

## Future Roadmap

- Clause-level citation mapping to internal policy IDs
- Human-in-the-loop approval workflows and ticketing integration
- Multi-regulator expansion (SEBI, RBI circular streams, MCA/GST)
- Continuous monitoring and auto-triggered re-analysis

## Team

Team ReguGuard AI

## License

MIT
