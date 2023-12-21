from .clients import client

class _ClientMixin:
    _base_url = "https://api.decart.ai/v1"
    _key_variable = "DECART_API_KEY"

class Decart(_ClientMixin, client.Client):
    pass

class AsyncDecart(_ClientMixin, client.AsyncClient):
    pass