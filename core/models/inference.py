from typing import Any

from core.models.base import BaseModel


class InferenceModel(BaseModel):
    prompt: str
    kwargs: dict[str, Any]
