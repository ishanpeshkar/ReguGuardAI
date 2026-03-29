from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.schema import ComplianceReport
from loguru import logger

class ReportGenerationAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, max_retries=0)

    def generate_summary(self, audit_data: dict):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Technical Writer. Summarize the compliance findings into a "
                       "professional report. Ensure the 'Action Items' are bulleted and clear."),
            ("user", "AUDIT DATA: {data}")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({"data": str(audit_data)})
            return response.content
        except Exception as exc:
            logger.warning(f"API Error: {exc}")
            return "Report generation unavailable (Rate Limit). Please wait 60 seconds."