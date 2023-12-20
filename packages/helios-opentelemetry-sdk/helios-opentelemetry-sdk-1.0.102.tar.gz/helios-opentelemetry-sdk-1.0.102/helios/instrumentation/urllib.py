import http.client
import urllib.request
from logging import getLogger

from opentelemetry.trace import Span

from helios.instrumentation.base_http_instrumentor import HeliosBaseHttpInstrumentor

_LOG = getLogger(__name__)


class HeliosUrllibInstrumentor(HeliosBaseHttpInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.urllib'
    INSTRUMENTOR_NAME = 'URLLibInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)

    def instrument(self, tracer_provider=None, **kwargs):
        if self.get_instrumentor() is None:
            return

        self.get_instrumentor().instrument(
            tracer_provider=tracer_provider, request_hook=self.request_hook, response_hook=self.response_hook)

    @staticmethod
    def request_hook(span: Span, request: urllib.request.Request):
        try:
            HeliosBaseHttpInstrumentor.base_request_hook(span, request.headers, None)
        except Exception as error:
            _LOG.debug('urllib request instrumentation error: %s.', error)

    @staticmethod
    def response_hook(span: Span, request: urllib.request.Request, response: http.client.HTTPResponse):
        try:
            data = request.data
            data_attr = HeliosBaseHttpInstrumentor.HTTP_REQUEST_BODY_ATTRIBUTE_NAME
            span.set_attribute(data_attr, data) if data else None
            # TODO: we're not extracting response body as it drains the data and makes it inaccessible later
            HeliosBaseHttpInstrumentor.base_response_hook(span, dict(response.headers), None)
        except Exception as error:
            _LOG.debug('urllib response instrumentation error: %s.', error)
