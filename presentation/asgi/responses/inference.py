from datetime import datetime

from pydantic import BaseModel


class InferenceFullResponse(BaseModel):
    prompt: str
    response: str
    json_data: str
    created_at: datetime
    updated_at: datetime
