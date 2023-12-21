import httpx

from .api_client import FireworksClient as FireworksClientV1
from .chat import Chat
from .completion import CompletionV2
from ._constants import DEFAULT_MAX_RETRIES
from typing import Mapping, Union
from .image import ImageInference, ImageInferenceV2

from abc import ABC, abstractmethod


class BaseFireworksClient:
    _organization: str
    _max_retries: int
    _client_v1: FireworksClientV1
    chat: Chat

    def __init__(
        self,
        *,
        api_key: Union[str, None] = None,
        base_url: Union[str, httpx.URL, None] = None,
        timeout: int = 600,
        account: str = "fireworks",
    ):
        self._client_v1 = FireworksClientV1(
            api_key=api_key, base_url=base_url, request_timeout=timeout
        )
        self._image_client_v1 = ImageInference(
            model=None,
            account=account,
            request_timeout=timeout,
            api_key=api_key,
            base_url=base_url,
        )

        self.completion = CompletionV2(self._client_v1, self.stream())
        self.chat = Chat(self._client_v1, self.stream())
        self.images = ImageInferenceV2(self._image_client_v1, self.stream())

        # TODO support the following
        # self.edits =
        # self.embeddings =
        # self.files =

        # self.audio
        # self.moderations
        # self.models
        # self.fine_tunes
        # self.beta

    @abstractmethod
    def stream(self) -> bool:
        pass


class FireworksClient(BaseFireworksClient):
    def stream(self) -> bool:
        return False


class AsyncFireworksClient(BaseFireworksClient):
    def stream(self) -> bool:
        return True
