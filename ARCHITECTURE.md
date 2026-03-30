# ReguGuard AI Architecture

## Purpose

ReguGuard AI is a multi-agent compliance intelligence system that ingests regulatory circulars, detects material changes, evaluates business applicability, scores risk, and generates an auditable summary for decision-makers. The design objective is to reduce review latency and cost while preserving governance controls expected in regulated banking and NBFC environments.

## Layered Architecture Overview

The platform is organized into four layers:

1. Ingestion Layer
2. Logic Layer
3. Guardrails Layer
4. Presentation Layer

This separation keeps document processing, reasoning, control mechanisms, and user experience independently evolvable.

## Layer 1: Ingestion Layer

Component: PDFProcessingEngine

Responsibilities:

- Read complex RBI and financial-regulator PDFs.
- Extract raw text from multi-page circulars.
- Normalize extracted content into a machine-usable text stream.
- Optionally chunk content for downstream indexing/vector workflows.

Implementation Notes:

- Uses pypdf for PDF parsing.
- Uses Gemini-compatible embeddings hooks for vector store creation when needed.
- Handles extraction from old vs new circular versions for side-by-side analysis.

Outcome:

A reliable, standardized text representation of each circular that can be used by downstream agents.

## Layer 2: Logic Layer (Multi-Agent Reasoning)

The core logic is implemented with five specialized agents orchestrated centrally.

### Agent 1: Ingestion Agent (The Librarian)

- Implemented by `PDFProcessingEngine` in `src/utils/pdf_engine.py`.
- Extracts text from old/new circular PDFs using `pypdf`.
- Supports chunking and FAISS embedding workflows for semantic retrieval extensions.
- Produces normalized text input for downstream reasoning agents.

### Agent 2: Change Detector (The Auditor)

- Compares old and new circular versions.
- Identifies differences in obligations, dates, thresholds, penalties, and scope.
- Produces a concise change summary for downstream risk and applicability checks.

### Agent 3: Compliance Reasoner (The Lawyer)

- Evaluates whether detected changes apply to a target entity profile.
- Reads business metadata (entity type, services, turnover, geography).
- Produces applicability rationale in plain language.

### Agent 4: Risk Scorer (The Analyst)

- Assigns operational/regulatory risk signal (for example: low, medium, high).
- Considers severity, implementation effort, and potential penalty exposure.
- Converts narrative findings into a prioritization cue for compliance teams.

### Agent 5: Report Generator (The Writer)

- Synthesizes outputs from all prior agents.
- Produces executive summary + action-oriented output.
- Formats response for analyst readability in the UI.

### Orchestrator (Control Plane)

Component: ReguGuardOrchestrator

Responsibilities:

- Coordinates agent call sequence.
- Passes intermediate artifacts between agents.
- Produces final response object:
  - report
  - audit_trail
- Centralizes workflow timing and operational logging.
- Applies deliberate cooldown waits between model-intensive calls to reduce quota/rate-limit failures.

Outcome:

A deterministic pipeline that turns raw regulatory documents into actionable, explainable compliance output.

## Layer 3: Guardrails Layer

Guardrails make the system safe and enterprise-usable.

### Applicability Guardrail

- Ensures output is scoped to the specific SME/bank profile instead of generic legal commentary.
- Prevents unnecessary remediation work on irrelevant clauses.
- Reduces false-positive compliance burden.

### Auditability Guardrail

- Captures reasoning artifacts in an audit trail object.
- Preserves intermediate context (applicability, detected changes, risk signal).
- Enables post-hoc review by compliance heads, risk teams, and auditors.

### Runtime Resilience Guardrail

- Try/except fallback in agents prevents full app failure on API errors/rate limits.
- Returns controlled fallback messages when model service is unavailable.
- Keeps the UI responsive and operational during transient model outages.
- LLM invocations are configured with low retry behavior for predictable failure handling.

Outcome:

Governed, reviewable outputs suitable for regulated workflows instead of opaque one-shot LLM answers.

## Layer 4: Presentation Layer

Component: Streamlit Dashboard (app.py)

Responsibilities:

- Collect profile and document inputs from users.
- Trigger compliance workflow from a single action.
- Display summary, detailed audit trail, and action items in separate tabs.
- Provide transparent visibility into AI-generated reasoning.

UX Characteristics:

- Role-oriented dashboard for compliance officers.
- Fast interaction loop for side-by-side regulation checks.
- Readable output blocks optimized for executive and analyst users.

Outcome:

A practical decision-support interface, not just a model endpoint.

## Data Flow Summary

1. User uploads old and new circular PDFs.
2. Ingestion layer extracts text from both documents.
3. Change Detector computes material diffs.
4. Compliance Reasoner checks business applicability.
5. Risk Scorer assigns prioritization signal.
6. Report Generator produces final narrative.
7. Orchestrator returns report + audit_trail to UI.
8. Dashboard presents findings for review and action.

## Design Benefits

- Speed: compresses review cycles from days to near real time.
- Cost: drastically lowers recurring analysis cost per circular.
- Consistency: standardized outputs across analysts and teams.
- Transparency: auditable reasoning for governance and controls.
- Resilience: graceful degradation when external LLM services are limited.

## Hackathon Criteria Mapping

- Domain expertise depth: finance-specific workflow for RBI circular deltas and applicability.
- Compliance/guardrails: profile-scoped reasoning, audit trail, and fallback controls.
- Edge-case handling: controlled behavior during missing context or model/API throttling.
- Full task completion: ingestion to final actionable report in one orchestrated run.
- Auditability: intermediate outputs are persisted in `audit_trail` and shown in dashboard tabs.

## Future Enhancements

- Policy mapping: map findings directly to internal policy IDs.
- Workflow integration: push action items into ticketing systems.
- Model strategy: route high-risk cases to stronger models selectively.
- Evaluation harness: benchmark agent outputs against legal SME labels.
- Fine-grained guardrails: clause-level confidence and escalation thresholds.
