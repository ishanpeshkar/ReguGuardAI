from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

class RiskScoringAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, max_retries=0)

    def assess_risk(self, changes: str, profile_json: str):
        logger.info("Assessing compliance risk level...")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Risk Management Consultant. Look at the regulatory changes "
                       "and the business profile. Rate the risk as HIGH, MEDIUM, or LOW. "
                       "Consider: Financial penalties, operational effort, and deadlines."),
            ("user", "CHANGES: {changes}\n\nBUSINESS: {profile}")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({"changes": changes, "profile": profile_json})
            return response.content
        except Exception as exc:
            logger.warning(f"API Error: {exc}")
            return "Risk scoring unavailable (Rate Limit). Please wait 60 seconds."