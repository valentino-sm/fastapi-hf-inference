from core.models.inference import InferenceModel
from infrastructure.db.repositories.inference import InferenceRepository
from infrastructure.db.session_manager import ABCSessionManager
from infrastructure.inference.huggingface import ABCExternalModel
from utils.logging import Logging


class InferenceService:
    """
    Business logic
    """

    def __init__(
        self,
        logging: Logging,
        model: ABCExternalModel,
        inference_repository: InferenceRepository,
        session_manager: ABCSessionManager,
    ) -> None:
        self._logger = logging.get_logger(__name__)
        self._model = model
        self._inference_repository = inference_repository
        self._session_manager = session_manager

    async def inference(self, request: InferenceModel) -> str:
        self._logger.debug(f"Request: {request}")
        response = self._model(request.prompt, **request.kwargs)
        async with self._session_manager():
            await self._inference_repository.save_inference(
                prompt=request.prompt,
                response=response,
                **request.kwargs,
            )
        return response

    async def get_all_inferences(self):
        async with self._session_manager():
            return await self._inference_repository.get_all_inferences()
