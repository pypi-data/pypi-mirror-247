from enum import Enum


class ModelState(str, Enum):
    ENABLED = "ENABLED"
    PENDING = "PENDING"
    DISABLED = "DISABLED"


class ModelVendor(str, Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    ANTHROPIC = "ANTHROPIC"
    LLMENGINE = "LLMENGINE"
    OTHER = "OTHER"


class ModelEndpointType(str, Enum):
    SYNC = "SYNC"
    ASYNC = "ASYNC"
    STREAMING = "STREAMING"
    BATCH = "BATCH"
