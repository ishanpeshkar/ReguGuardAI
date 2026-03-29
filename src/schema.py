from pydantic import BaseModel, Field
from typing import List, Optional

class SMEProfile(BaseModel):
    """The profile of the business being checked for compliance."""
    company_name: str
    entity_type: str  # e.g., NBFC, Fintech, Bank
    services: List[str]
    annual_turnover: str
    location: str = "India"

class RegulatoryChange(BaseModel):
    """Represents a specific change found between two document versions."""
    section: str
    old_requirement: Optional[str] = "New Section Added"
    new_requirement: str
    impact_level: str  # High, Medium, Low
    reasoning: str  # Why did the AI flag this?

class ComplianceReport(BaseModel):
    """The final output generated for the user."""
    is_applicable: bool
    summary: str
    detected_changes: List[RegulatoryChange]
    action_items: List[str]
    audit_trail: str # Steps taken by agents to reach this conclusion