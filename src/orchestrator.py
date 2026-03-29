import time
from src.utils.pdf_engine import PDFProcessingEngine
from src.agents.change_detector import ChangeDetectionAgent
from src.agents.compliance_reasoner import ComplianceReasoningAgent
from src.agents.risk_agent import RiskScoringAgent
from src.agents.report_agent import ReportGenerationAgent
from src.schema import SMEProfile
from loguru import logger

class ReguGuardOrchestrator:
    def __init__(self):
        self.engine = PDFProcessingEngine()
        self.detector = ChangeDetectionAgent()
        self.reasoner = ComplianceReasoningAgent()
        self.risker = RiskScoringAgent()
        self.reporter = ReportGenerationAgent()

    def run_compliance_check(self, old_pdf: str, new_pdf: str, profile: SMEProfile):
        logger.info(f"🚀 Starting Compliance Workflow for {profile.company_name}")

        # 1. Ingest
        old_text = self.engine.extract_text(old_pdf)
        new_text = self.engine.extract_text(new_pdf)
        
        # 2. Detect Changes
        changes = self.detector.compare_documents(old_text[:8000], new_text[:8000])
        logger.info("Waiting 10s for API quota...")
        time.sleep(10) # Pause to reset Gemini rate limit

        # 3. Reason Applicability
        applicability = self.reasoner.check_applicability(profile, new_text[:8000])
        logger.info("Waiting 10s for API quota...")
        time.sleep(10)
        
        # 4. Score Risk
        risk_level = self.risker.assess_risk(changes, profile.model_dump_json())
        time.sleep(5)

        # 5. Final Report
        audit_data = {
            "profile": profile.company_name,
            "applicability": applicability,
            "detected_changes": changes,
            "risk_evaluation": risk_level
        }
        
        final_report = self.reporter.generate_summary(audit_data)
        
        return {
            "report": final_report,
            "audit_trail": audit_data
        }