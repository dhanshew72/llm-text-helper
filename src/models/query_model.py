from pydantic import BaseModel


class QueryModel(BaseModel):
    user: str
    question: str
