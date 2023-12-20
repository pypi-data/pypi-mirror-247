from sys import modules
from logging import getLogger

import wrapt

from opentelemetry.util.http import parse_excluded_urls

from helios.instrumentation.base_http_instrumentor import HeliosBaseHttpInstrumentor
from helios.instrumentation.helios_asgi_middleware import HeliosAsgiMiddleware

_LOG = getLogger(__name__)


class HeliosStarletteInstrumentor(HeliosBaseHttpInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.starlette'
    INSTRUMENTOR_NAME = 'StarletteInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)
        self.tracer_provider = None
        self.instrumented_apps = set()

    def instrument(self, tracer_provider=None, **kwargs):
        if self.get_instrumentor() is None:
            return

        self.tracer_provider = tracer_provider
        self.excluded_urls = kwargs.get('excluded_urls')

        wrapt.wrap_function_wrapper('opentelemetry.instrumentation.starlette', '_get_default_span_details', HeliosAsgiMiddleware.get_span_details_wrapper)
        wrapt.wrap_function_wrapper('starlette.applications', 'Starlette.__init__', self.starlette_instrument_and_run)

    def uninstrument(self):
        if self.get_instrumentor() is None:
            return

        for app in self.instrumented_apps:
            self.get_instrumentor().uninstrument()
        self.instrumented_apps = set()

    def starlette_instrument_and_run(self, wrapped, instance, args, kwargs):
        res = wrapped(*args, **kwargs)

        # starlette instrumentation holds excluded_urls as a module var rather than taking in an arg to instrument()
        if modules[HeliosStarletteInstrumentor.MODULE_NAME] is not None:
            setattr(modules[HeliosStarletteInstrumentor.MODULE_NAME], '_excluded_urls', parse_excluded_urls(self.excluded_urls))

        try:
            if instance not in self.instrumented_apps:
                self.instrumented_apps.add(instance)
                self.get_instrumentor().instrument_app(
                    instance,
                    # server_request_hook=self.server_request_hook,
                    # client_request_hook=self.client_request_hook,
                    # client_response_hook=self.client_response_hook,
                    tracer_provider=self.tracer_provider
                )
                get_span_details = HeliosBaseHttpInstrumentor.import_attribute(self.MODULE_NAME, '_get_default_span_details')
                instance.add_middleware(
                    HeliosAsgiMiddleware,
                    tracer=self.tracer_provider.get_tracer(self.MODULE_NAME),
                    excluded_urls=self.excluded_urls,
                    get_span_details=get_span_details
                )
        except Exception as error:
            _LOG.debug('starlette __init__ instrumentation error: %s.', error)

        return res
