from src.orchestrator import ReguGuardOrchestrator
from src.schema import SMEProfile
from dotenv import load_dotenv

load_dotenv()

def main():
    orchestrator = ReguGuardOrchestrator()
    
    # Use your actual file paths here
    old_pdf = "data/raw_pdfs/RBI Internal Ombudsman 2023.pdf"
    new_pdf = "data/raw_pdfs/RBI Internal Ombudsman 2026.pdf"
    
    bank_profile = SMEProfile(
        company_name="Bharat Heritage Bank",
        entity_type="Commercial Bank",
        services=["Retail Banking", "Loans"],
        annual_turnover="15000 Cr"
    )

    results = orchestrator.run_compliance_check(old_pdf, new_pdf, bank_profile)
    
    print("\n" + "="*50)
    print("FINAL COMPLIANCE REPORT")
    print("="*50)
    print(results['report'])
    print("\n" + "="*50)
    print("AUDIT TRAIL (AI REASONING)")
    print(results['audit_trail']['risk_evaluation'])

if __name__ == "__main__":
    main()