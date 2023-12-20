from logging import getLogger
from typing import Dict, List, Tuple
from io import BytesIO
import wrapt
from opentelemetry.semconv.trace import SpanAttributes

from opentelemetry.trace import Span

from helios.instrumentation.base_http_instrumentor import HeliosBaseHttpInstrumentor

_LOG = getLogger(__name__)
REQUEST_ATTRIBUTE = 'request_object'


class HeliosFlaskInstrumentor(HeliosBaseHttpInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.flask'
    INSTRUMENTOR_NAME = 'FlaskInstrumentor'
    RESPONSE_BODY_HEADER_NAME = 'HS-Response-body'
    FLASK_REQUEST_VAR_NAME = 'werkzeug.request'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)
        self.tracer_provider = None
        self.excluded_urls = None
        self.instrumented_apps = set()

    def instrument(self, tracer_provider=None, **kwargs):
        if self.get_instrumentor() is None:
            return

        self.tracer_provider = tracer_provider
        self.excluded_urls = kwargs.get('excluded_urls')
        wrapt.wrap_function_wrapper('flask', 'Flask.__init__', self.flask_instrument_and_run)

    def uninstrument(self):
        if self.get_instrumentor() is None:
            return

        for app in self.instrumented_apps:
            self.get_instrumentor().uninstrument_app(app)
        self.instrumented_apps = set()

    def flask_instrument_and_run(self, wrapped, instance, args, kwargs):
        res = wrapped(*args, **kwargs)

        try:
            if instance not in self.instrumented_apps:
                self.instrumented_apps.add(instance)
                instance.after_request(self.flask_response_callback)
                self.get_instrumentor().instrument_app(
                    instance,
                    tracer_provider=self.tracer_provider,
                    request_hook=self.request_hook,
                    response_hook=self.response_hook,
                    excluded_urls=self.excluded_urls
                )
        except Exception as error:
            _LOG.debug('flask __init__ instrumentation error: %s.', error)

        return res

    @staticmethod
    def _has_multipart_content_type(request):
        content_type = getattr(request, 'content_type', None)
        if content_type is None:
            return False

        return content_type.startswith('multipart')

    @staticmethod
    def request_hook(span: Span, flask_request_environ: Dict) -> None:
        try:
            if span is None:
                return

            request = flask_request_environ.get(HeliosFlaskInstrumentor.FLASK_REQUEST_VAR_NAME)
            setattr(span, REQUEST_ATTRIBUTE, request)

            # backup the stream contents to allow consuming both by app and instrumentation
            if HeliosFlaskInstrumentor._has_multipart_content_type(request):
                length = request.content_length or 0
                request_body = request.environ['wsgi.input'].read(length)
                request.environ['request_body_copy'] = request_body
                request.environ['wsgi.input'] = BytesIO(request_body)
        except Exception as error:
            _LOG.debug('flask request instrumentation error: %s.', error)

    @staticmethod
    def extract_request_body(request):
        if HeliosFlaskInstrumentor._has_multipart_content_type(request):
            try:
                return bytearray(request.environ['request_body_copy'])
            except Exception:
                return None

        try:
            # Protect with try/catch to avoid cases where json could not be parsed, causing an exception
            request_body = request.json
            if request_body:
                return request_body
        except Exception as e:
            _LOG.debug('Could not extract json bodyL %s', e)

        return request.data

    @staticmethod
    def handle_request_attributes(span: Span, request):
        if request:
            url = request.url
            request_body = HeliosFlaskInstrumentor.extract_request_body(request)
        else:
            url = None
            request_body = None

        span.set_attribute(SpanAttributes.HTTP_URL, url) if url else None
        HeliosFlaskInstrumentor.base_request_hook(span, dict(request.headers), request_body)

    @staticmethod
    def response_hook(span: Span, status: str, response_headers: List[Tuple[str]]) -> None:
        try:
            if span is None:
                return

            request = getattr(span, REQUEST_ATTRIBUTE)
            HeliosFlaskInstrumentor.handle_request_attributes(span, request)

            response_body = None
            resp_headers = dict()

            for header in response_headers:
                if len(header) != 2:
                    continue
                key, value = header
                if key == HeliosFlaskInstrumentor.RESPONSE_BODY_HEADER_NAME:
                    response_body = value
                    response_headers.remove(header)
                else:
                    resp_headers[key] = value

            HeliosFlaskInstrumentor.base_response_hook(span, resp_headers, response_body)
        except Exception as error:
            _LOG.debug('flask response instrumentation error: %s.', error)

    @staticmethod
    def flask_response_callback(response):
        try:
            if response is None:
                return None
            body = response.data
            body = response.json if body is None else body
            if body is None:
                return response
            if type(body) == bytes:
                body = body.decode()
            body = body.replace("\n", " ")
            response.headers.add(HeliosFlaskInstrumentor.RESPONSE_BODY_HEADER_NAME, body)
        except Exception as error:
            _LOG.debug('flask after_request instrumentation error: %s.', error)

        return response
