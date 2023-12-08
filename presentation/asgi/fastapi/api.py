from fastapi import APIRouter, Depends

from core.models.inference import InferenceModel
from core.services.inference import InferenceService
from presentation.asgi.fastapi.abc_router import ABCRouterBuilder
from presentation.asgi.requests.inference import InferenceRequest
from presentation.asgi.responses.inference import InferenceFullResponse
from utils.logging import Logging


class APIRouterBuilder(ABCRouterBuilder):
    def __init__(
        self,
        logging: Logging,
        inference_service: InferenceService,
    ) -> None:
        self._logging = logging
        self._logger = logging.get_logger(__name__)
        self._inference_service = inference_service

    def create_router(self) -> APIRouter:
        router = APIRouter(prefix="/api/v1", tags=["API v1"])

        @router.post("/inference")
        async def _(inference_request: InferenceRequest = Depends()):
            """
            Inference API Endpoint
            """
            return await self._inference_service.inference(
                InferenceModel(
                    prompt=inference_request.prompt,
                    kwargs=inference_request.model_dump(exclude={"prompt"}),
                ),
            )

        @router.get("/inference", response_model=list[InferenceFullResponse])
        async def _():
            """
            Get all inferences
            """
            return await self._inference_service.get_all_inferences()

        return router
