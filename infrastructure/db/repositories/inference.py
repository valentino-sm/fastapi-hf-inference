import json
from typing import Any, TypeVar

from infrastructure.db.abc_repository import BaseRepository
from infrastructure.db.models.inference import Inference

T = TypeVar("T")


class InferenceRepository:
    def __init__(
        self,
        repository: BaseRepository,  # type: ignore - hack for DI
    ) -> None:
        self._repository: BaseRepository[Inference] = repository

    async def save_inference(
        self, prompt: str, response: str, **kwargs: Any
    ) -> Inference:
        return await self._repository.create_obj(
            Inference, prompt=prompt, response=response, json_data=json.dumps(kwargs)
        )
