import time
from functools import wraps
from typing import Any, Callable, ParamSpec, Protocol, TypeVar

import numpy as np
import torch
from transformers import AutoModelForCausalLM  # type: ignore
from transformers import AutoTokenizer  # type: ignore

np.random.seed(42)
torch.manual_seed(42)


T = TypeVar("T")
P = ParamSpec("P")


def timeit(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def timeit_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


class ABCExternalModel(Protocol):
    def __call__(self, prompt: str, **kwargs: Any) -> str:
        raise NotImplementedError


class HuggingFaceModel(ABCExternalModel):
    def __init__(
        self, model_path: str, tokenizer_path: str, device: str = "cpu"
    ) -> None:
        # self._model = GPT2LMHeadModel.from_pretrained(model_path)
        # self._tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
        self._model = AutoModelForCausalLM.from_pretrained(model_path)
        self._tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self._device = device
        # self._model.to(device)

    @timeit
    def __call__(self, prompt: str, **kwargs: Any) -> str:
        if "pad_token_id" not in kwargs:
            kwargs["pad_token_id"] = self._tokenizer.eos_token_id
        input_ids = self._tokenizer.encode(prompt, return_tensors="pt")
        outputs = self._model.generate(input_ids, **kwargs)
        result = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        if not isinstance(result, str):
            raise ValueError(f"Unexpected result type: {type(result)}")
        return result
