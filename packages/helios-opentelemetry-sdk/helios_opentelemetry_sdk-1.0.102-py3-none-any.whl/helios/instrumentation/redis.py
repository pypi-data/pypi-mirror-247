import json
from logging import getLogger

from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Span

from helios.instrumentation.base import HeliosBaseInstrumentor

_LOG = getLogger(__name__)


class HeliosRedisInstrumentor(HeliosBaseInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.redis'
    INSTRUMENTOR_NAME = 'RedisInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)

    def instrument(self, tracer_provider=None, **kwargs):
        if self.get_instrumentor() is None:
            return

        self.get_instrumentor().instrument(tracer_provider=tracer_provider,
                                           request_hook=self.request_hook,
                                           response_hook=self.response_hook)

    def request_hook(self, span: Span, connection, args, kwargs):
        # Default state serialization truncates it after 100 chars, so we override the behavior
        db_statement = ' '.join([str(arg) for arg in args])
        span.set_attribute(SpanAttributes.DB_STATEMENT, db_statement)
        span.set_attribute(SpanAttributes.DB_SYSTEM, 'redis')

    def response_hook(self, span: Span, connection, response):
        if not span or not span.is_recording():
            return

        try:
            query_result = None
            response_type = type(response)
            if response_type in [str, int, bool, float]:
                query_result = response
            elif response_type == bytes:
                query_result = response.decode()
            elif response_type in [tuple, dict, list]:
                query_result = json.dumps(response)

            HeliosBaseInstrumentor.set_payload_attribute(span, self.DB_QUERY_RESULT_ATTRIBUTE_NAME, query_result)

        except Exception as error:
            _LOG.debug('redis response instrumentation error: %s.', error)
