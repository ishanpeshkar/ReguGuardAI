from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

class ChangeDetectionAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, max_retries=0)

    def compare_documents(self, old_text: str, new_text: str):
        logger.info("Comparing document versions for changes...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Senior Regulatory Compliance Officer. "
                       "Compare the OLD vs NEW regulation. Identify specific changes in "
                       "deadlines, applicability, and penalties. "
                       "Format the output as a clean summary."),
            ("user", "OLD VERSION: {old}\n\nNEW VERSION: {new}")
        ])

        chain = prompt | self.llm
        # Gemini can handle a lot of text, but we'll send a focused summary
        try:
            response = chain.invoke({
                "old": old_text[:15000], # Taking a large slice
                "new": new_text[:15000]
            })
            return response.content
        except Exception as exc:
            logger.warning(f"API Error: {exc}")
            return "Change detection unavailable (Rate Limit). Please wait 60 seconds."