import os
import httpx
from ..resources import chat
from ..resources import completions
from . import base_client
from .. import exceptions


class _ClientMixin:
    _base_url: httpx.URL
    _key_variable: str

    def _make_status_error(self, response: httpx.Response) -> exceptions.APIError:
        # TODO(vova): based on code
        return exceptions.APIError()

class Client(_ClientMixin, base_client.BaseClient):
    def __init__(self, api_key: str | None = None) -> None:
        if api_key is None:
            api_key = os.getenv(self._key_variable)

        self.chat = chat.Chat(self)
        self.completion = completions.Completions(self)

        super().__init__(
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            base_url=httpx.URL(self._base_url),
        )


class AsyncClient(_ClientMixin, base_client.AsyncBaseClient):
    def __init__(self, api_key: str | None = None) -> None:
        if api_key is None:
            api_key = os.getenv(self._key_variable)

        self.chat = chat.AsyncChat(self)
        self.completion = completions.AsyncCompletions(self)

        super().__init__(
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            base_url=httpx.URL(self._base_url),
        )
