from typing import List

from .completions_shared import CompletionBaseRequest, CompletionBaseResponse


class CompletionRequest(CompletionBaseRequest):
    prompt: str


class CompletionResponse(CompletionBaseResponse):
    completions: List[str]
