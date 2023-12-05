from pydantic import BaseModel


class InferenceResponse(BaseModel):
    text: str
