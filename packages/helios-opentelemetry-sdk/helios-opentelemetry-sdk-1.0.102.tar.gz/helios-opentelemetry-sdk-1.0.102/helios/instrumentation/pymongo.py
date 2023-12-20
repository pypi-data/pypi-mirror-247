import json
from logging import getLogger

from opentelemetry.trace import Span

try:
    from bson import json_util
except ModuleNotFoundError:
    json_util = json

from helios.instrumentation.base import HeliosBaseInstrumentor

_LOG = getLogger(__name__)


class HeliosPymongoInstrumentor(HeliosBaseInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.pymongo'
    INSTRUMENTOR_NAME = 'PymongoInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)

    def instrument(self, tracer_provider=None, **kwargs):
        if self.get_instrumentor() is None:
            return

        self.get_instrumentor().instrument(tracer_provider=tracer_provider, response_hook=self.response_hook)

    def uninstrument(self):
        super().uninstrument()
        if self.get_instrumentor():
            self.get_instrumentor()._commandtracer_instance = None

    def response_hook(self, span: Span, event):
        try:
            # event is an object of type `pymongo.CommandSucceededEvent`
            if span and span.is_recording():
                reply_document = getattr(event, 'reply', {})
                reply = json_util.dumps(reply_document)
                HeliosBaseInstrumentor.set_payload_attribute(span, self.DB_QUERY_RESULT_ATTRIBUTE_NAME, reply)
        except Exception as error:
            _LOG.debug('pymongo response instrumentation error: %s.', error)
