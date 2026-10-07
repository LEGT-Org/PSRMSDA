from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.llm_diagnosis.model import LLMDiagnosis


class LLMDiagnosisRepository:

    def __init__(self, db: Session):

        self.db = db

    def create(self, llm_diagnosis: LLMDiagnosis):
        
        self.db.add(llm_diagnosis)
        return llm_diagnosis