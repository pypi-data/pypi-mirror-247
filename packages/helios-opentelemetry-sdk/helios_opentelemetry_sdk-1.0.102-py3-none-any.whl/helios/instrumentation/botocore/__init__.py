from logging import getLogger

from helios.instrumentation.base import HeliosBaseInstrumentor
from helios.instrumentation.botocore.consts import AwsAttribute
from helios.instrumentation.botocore.dynamodb import DynamoDBInstrumentor
from helios.instrumentation.botocore.eventbridge import EventBridgeInstrumentor
from helios.instrumentation.botocore.s3 import S3Instrumentor
from helios.instrumentation.botocore.ses import SESInstrumentor
from helios.instrumentation.botocore.sns import SNSInstrumentor
from helios.instrumentation.botocore.sqs import SQSInstrumentor
from helios.instrumentation.urllib3 import HeliosUrllib3Instrumentor
from opentelemetry.context import _SUPPRESS_INSTRUMENTATION_KEY
from wrapt import wrap_function_wrapper

from opentelemetry import context

_LOG = getLogger(__name__)


class HeliosBotocoreInstrumentor(HeliosBaseInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.botocore'
    INSTRUMENTOR_NAME = 'BotocoreInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)
        self.services = dict()
        self.context_token = None

    def suppress_urllib3(self, wrapped, instance, args, kwargs):
        try:
            context_token = context.attach(context.set_value(_SUPPRESS_INSTRUMENTATION_KEY, True))
            return wrapped(*args, **kwargs)
        finally:
            if context_token:
                context.detach(context_token)

    def instrument(self, tracer_provider=None, **kwargs):

        if self.get_instrumentor() is None:
            return

        self.services.update({
            'dynamodb': DynamoDBInstrumentor(),
            's3': S3Instrumentor(),
            'ses': SESInstrumentor(),
            'sns': SNSInstrumentor(),
            'sqs': SQSInstrumentor(tracer_provider=tracer_provider),
            'events': EventBridgeInstrumentor(),
        })

        # Avoid instrumenting credentials retrieval requests
        wrap_function_wrapper('botocore.httpsession', 'URLLib3Session.send', self.suppress_urllib3)

        self.get_instrumentor().instrument(
            tracer_provider=tracer_provider,
            response_hook=self.response_hook,
            request_hook=self.request_hook
        )

    def request_hook(self, span, service_name, operation_name, api_params):
        try:
            if not span or not span.is_recording():
                return

            # botocore uses urllib3, which is also instrumented. We add urllib3's HTTP key to
            # the context, which is later checked on and suppresses further instrumentations.
            suppress_key = (
                HeliosBaseInstrumentor.import_attribute(
                    HeliosUrllib3Instrumentor.MODULE_NAME,
                    '_SUPPRESS_HTTP_INSTRUMENTATION_KEY'
                )
            )
            if suppress_key:
                self.context_token = context.attach(context.set_value(suppress_key, True))

            span.set_attribute(AwsAttribute.AWS_SERVICE, service_name)
            span.set_attribute(AwsAttribute.AWS_OPERATION, operation_name)
            service_instrumentor = self.services.get(service_name)
            if service_instrumentor is not None:
                if callable(service_instrumentor.request_hook):
                    return service_instrumentor.request_hook(span, operation_name, api_params)
        except Exception as error:
            _LOG.debug('botocore request instrumentation error: %s.', error)

    def response_hook(self, span, service_name, operation_name, result):
        try:
            if not span or not span.is_recording():
                return

            if self.context_token:
                context.detach(self.context_token)

            span.set_attribute(AwsAttribute.AWS_SERVICE, service_name)
            service_instrumentor = self.services.get(service_name)
            if service_instrumentor is not None:
                if callable(service_instrumentor.response_hook):
                    return service_instrumentor.response_hook(span, operation_name, result)
        except Exception as error:
            _LOG.debug('botocore response instrumentation error: %s.', error)
