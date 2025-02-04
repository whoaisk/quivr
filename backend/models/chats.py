from typing import List, Tuple, Optional
from uuid import UUID

from pydantic import BaseModel


class ChatMessage(BaseModel):
    model: str = "gpt-3.5-turbo"
    question: str
    # A list of tuples where each tuple is (speaker, text)
    history: List[Tuple[str, str]]
    temperature: float = 0.4
    max_tokens: int = 384
    use_summarization: bool = False
    chat_id: Optional[UUID] = None, 
