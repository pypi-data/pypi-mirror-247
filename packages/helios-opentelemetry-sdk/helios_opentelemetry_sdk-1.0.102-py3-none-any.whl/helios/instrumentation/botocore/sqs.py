import json
from opentelemetry import trace
from opentelemetry.propagate import inject
from typing import Dict

from opentelemetry.sdk.trace import Span
from opentelemetry.trace import set_span_in_context, SpanKind
from opentelemetry.semconv.trace import SpanAttributes, MessagingOperationValues

from helios.instrumentation.botocore.consts import AwsAttribute, AwsOperation, AwsParam, AwsService, \
    INJECTED_MESSAGE_ATTRIBUTE_NAMES
from helios.instrumentation.botocore.sqs_message_context import SqsMessageContext
from helios.instrumentation.botocore.utils import SQSContextSetter


class SQSInstrumentor(object):
    def __init__(self, tracer_provider=None):
        self.tracer_provider = tracer_provider
        self.tracer = trace.get_tracer(
            __name__, tracer_provider=tracer_provider
        )

    def request_hook(self, span: Span, operation_name: str, api_params: Dict):
        if api_params is None:
            return

        self.set_queue_attributes(api_params, span)
        if operation_name == AwsOperation.SEND_MESSAGE:
            api_params[AwsParam.MESSAGE_ATTRIBUTES] = self.handle_outgoing_message(span, api_params)
        elif operation_name == AwsOperation.SEND_MESSAGE_BATCH:
            for entry in api_params.get(AwsParam.ENTRIES, []):
                entry[AwsParam.MESSAGE_ATTRIBUTES] = self.handle_outgoing_message(span, entry)
            span.set_attribute(AwsAttribute.MESSAGING_PAYLOAD, json.dumps(api_params.get('Entries')))
        elif operation_name == AwsOperation.RECEIVE_MESSAGE:
            message_attribute_names = api_params.get(AwsParam.MESSAGE_ATTRIBUTE_NAMES, [])
            span.set_attribute(SpanAttributes.MESSAGING_OPERATION, MessagingOperationValues.RECEIVE.value)
            message_attribute_names.extend(INJECTED_MESSAGE_ATTRIBUTE_NAMES)
            api_params[AwsParam.MESSAGE_ATTRIBUTE_NAMES] = message_attribute_names

    def response_hook(self, span: Span, operation_name: str, result: Dict):
        if result is None:
            return

        if operation_name == AwsOperation.RECEIVE_MESSAGE:
            for message in result.get(AwsParam.MESSAGES):
                if message is None:
                    continue
                with SqsMessageContext(message):
                    span_name = f'SQS {operation_name}'
                    message_span = self.tracer.start_span(span_name, kind=SpanKind.CONSUMER)
                    message_span.set_attributes(span._attributes)
                    message_span.set_attribute(AwsAttribute.MESSAGING_PAYLOAD, message.get(AwsParam.BODY))
                    message_attributes = message.get(AwsParam.MESSAGE_ATTRIBUTES)
                    if message_attributes:
                        message_span.set_attribute(AwsAttribute.SQS_MESSAGE_ATTRIBUTES, json.dumps(message_attributes))
                    message_span.end()

    def handle_outgoing_message(self, span, message_data):
        message_body = message_data.get(AwsParam.MESSAGE_BODY)
        message_attributes = message_data.get(AwsParam.MESSAGE_ATTRIBUTES, dict())
        if message_body:
            span.set_attribute(AwsAttribute.MESSAGING_PAYLOAD, message_body)
        if message_attributes:
            span.set_attribute(AwsAttribute.SQS_MESSAGE_ATTRIBUTES, json.dumps(message_attributes))

        inject(message_attributes, context=set_span_in_context(span), setter=SQSContextSetter())
        return message_attributes

    def set_queue_attributes(self, api_params, span):
        queue_name = api_params.get(AwsParam.QUEUE_NAME)
        queue_url = api_params.get(AwsParam.QUEUE_URL)
        if not queue_name and queue_url:
            queue_name = self.extract_queue_name(queue_url)
        attributes = {
            SpanAttributes.MESSAGING_SYSTEM: AwsService.SQS,
            SpanAttributes.MESSAGING_OPERATION: MessagingOperationValues.PROCESS.value
        }
        if queue_name:
            attributes[SpanAttributes.MESSAGING_DESTINATION] = queue_name
        if queue_url:
            attributes[SpanAttributes.MESSAGING_URL] = queue_url
        span.set_attributes(attributes)

    def extract_queue_name(self, queue_url):
        return queue_url.split('/').pop()
