from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.schema import SMEProfile
from loguru import logger

class ComplianceReasoningAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, max_retries=0)

    def check_applicability(self, profile: SMEProfile, regulation_text: str):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Analyze if this regulation applies to the following business. "
                       "Look for 'Applicability' or 'Scope' sections in the text."),
            ("user", "BUSINESS: {profile}\n\nREGULATION: {reg}")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "profile": profile.model_dump_json(),
                "reg": regulation_text[:15000]
            })
            return response.content
        except Exception as exc:
            logger.warning(f"API Error: {exc}")
            return "Applicability check unavailable (Rate Limit). Please wait 60 seconds."