from pydantic.main import BaseModel


class InferenceRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_length: int = 50
    top_p: float = 0.95
    top_k: int = 5
    repetition_penalty: float = 5.0
    do_sample: bool = True
    num_beams: int = 10
    no_repeat_ngram_size: int = 3
