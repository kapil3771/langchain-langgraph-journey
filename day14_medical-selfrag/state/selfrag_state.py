from typing import List, Optional, Literal
from langchain_core.messages import BaseMessage
from pydantic import BaseModel

class SelfRAGState(BaseModel):
    question : str

    retrieved_docs : List[str] = []
    corrected_docs : Optional[list[str]] = None

    final_context : str = ""
    answer : str = ""

    grade : Literal["correct", "ambiguous", "incorrect"] = "incorrect"
    reflection_token : Literal["ISREL", "ISUSE", "ISSUP"] = "ISREL"
    feedback : str = ""
    correction_reason : Optional[str] = None

    trusted_docs :Optional[List[str]] = None
    hallucination_spans: Optional[List[str]] = None

    logs : List[str] = []
    messages : List[BaseMessage] = []
    retry_count : int = 0
