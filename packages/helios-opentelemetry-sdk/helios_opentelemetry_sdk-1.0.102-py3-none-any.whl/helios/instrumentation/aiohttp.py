from logging import getLogger

from opentelemetry.trace import Span
from helios.instrumentation.base_http_instrumentor import HeliosBaseHttpInstrumentor

_LOG = getLogger(__name__)


class HeliosAiohttpInstrumentor(HeliosBaseHttpInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.aiohttp_client'
    INSTRUMENTOR_NAME = 'AioHttpClientInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)

    def instrument(self, tracer_provider=None, **kwargs):
        if self.get_instrumentor() is None:
            return

        self.get_instrumentor().instrument(
            tracer_provider=tracer_provider,
            request_hook=self.request_hook,
            response_hook=self.response_hook
        )

    def request_hook(self, span: Span, requestInfo):
        try:
            HeliosBaseHttpInstrumentor.base_request_hook(span, dict(requestInfo.headers), None)
        except Exception as error:
            _LOG.debug('aiohttp request instrumentation error: %s.', error)

    def response_hook(self, span: Span, requestEndInfo):
        try:
            HeliosBaseHttpInstrumentor.base_response_hook(span, dict(requestEndInfo.response.headers), None)
        except Exception as error:
            _LOG.debug('aiohttp response instrumentation error: %s.', error)
