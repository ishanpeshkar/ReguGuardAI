# ReguGuard AI

AI-powered regulatory compliance assistant for banks, NBFCs, and fintech teams.

ReguGuard AI compares old vs new regulatory circulars, evaluates business applicability, scores risk, and generates a transparent audit trail in a Streamlit dashboard.

## What It Does

- Extracts text from uploaded regulatory PDFs.
- Detects policy changes between document versions.
- Checks applicability against SME/business profiles.
- Scores compliance risk level.
- Generates a final report with audit-ready reasoning.
- Handles API/rate-limit failures gracefully so the app does not crash.

## Tech Stack

- Python 3.14
- Streamlit
- LangChain
- Google Gemini (via `langchain-google-genai`)
- Pydantic
- PyPDF

## Project Structure

```text
reguguard_ai/
|-- app.py
|-- test_run.py
|-- requirements.txt
|-- .gitignore
|-- ARCHITECTURE.md
|-- IMPACT_MODEL.md
|-- src/
|   |-- __init__.py
|   |-- main.py
|   |-- orchestrator.py
|   |-- schema.py
|   |-- agents/
|   |   |-- __init__.py
|   |   |-- change_detector.py
|   |   |-- compliance_reasoner.py
|   |   |-- risk_agent.py
|   |   |-- report_agent.py
|   |-- utils/
|       |-- pdf_engine.py
|-- data/
|   |-- profiles/
|   |   |-- fintech_startup.json
|   |   |-- nbfc_small.json
|   |   |-- private_bank_mid.json
|   |-- raw_pdfs/
|       |-- RBI Internal Ombudsman 2023.pdf
|       |-- RBI Internal Ombudsman 2026.pdf
|       |-- RBI Prudential Norms on Declaration 2026.pdf
```

## Setup

1. Create and activate virtual environment.

```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file at project root.

```env
GEMINI_API_KEY=your_api_key_here
# or
# GOOGLE_API_KEY=your_api_key_here
```

## Run

### Streamlit App

```powershell
streamlit run app.py
```

### CLI Test Script

```powershell
python test_run.py
```

## How The Pipeline Works

1. `PDFProcessingEngine` extracts text from old and new PDFs.
2. `ChangeDetectionAgent` identifies material regulatory differences.
3. `ComplianceReasoningAgent` checks if changes apply to the selected profile.
4. `RiskScoringAgent` estimates business/compliance risk.
5. `ReportGenerationAgent` compiles the final summary.
6. `ReguGuardOrchestrator` coordinates all steps and returns an audit trail.

## Notes

- If your Gemini API quota is exhausted, the app returns fallback messages instead of crashing.
- The warning about Pydantic v1 compatibility on Python 3.14 is currently non-blocking.

## Supporting Docs

- `ARCHITECTURE.md`: layered architecture and design rationale.
- `IMPACT_MODEL.md`: quantified business impact and savings model.

## Hackathon Value Proposition

- Near real-time circular analysis.
- Large cost reduction vs manual legal review.
- Better governance through transparent audit trail.
- Practical UI for compliance and risk teams.
