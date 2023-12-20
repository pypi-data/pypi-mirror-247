"""
Instrument `kafka-python` to report instrumentation-kafka produced and consumed messages

Usage
-----

..code:: python

    from hs_sdk.src.instrumentation.kafka import KafkaInstrumentor
    from kafka import KafkaProducer, KafkaConsumer

    # Instrument kafka
    KafkaInstrumentor().instrument()

    # This will report a span of type producer with the default settings
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    producer.send('my-topic', b'raw_bytes')


    # This will report a span of type consumer with the default settings
    consumer = KafkaConsumer('my-topic',
                             group_id='my-group',
                             bootstrap_servers=['localhost:9092'])
    for message in consumer:
        # process message

API
___
"""

import json
import time
from logging import getLogger
from typing import Collection, Optional, List

from opentelemetry.context import attach, detach
from wrapt import wrap_function_wrapper
import kafka

from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Tracer, set_span_in_context
from opentelemetry.propagate import inject, extract
from opentelemetry.propagators import textmap

from helios.kafka_instrumentation.src.kafka.package import _instruments

__version__ = "0.1.0"

PRODUCER_SPAN_NAME = "kafka.send"
CONSUMER_SPAN_NAME = "kafka.consume"

SPAN_ATTRIBUTES_MESSAGING_PAYLOAD = "messaging.payload"
SPAN_ATTRIBUTES_MESSAGING_KAFKA_HEADERS = "messaging.kafka.headers"

_LOG = getLogger(__name__)


class KafkaContextGetter(textmap.Getter):
    def get(self, carrier: textmap.CarrierT, key: str) -> Optional[List[str]]:
        if carrier is None:
            return None

        for k, v in carrier:
            if k == key:
                if v is not None:
                    return [v.decode()]
        return None

    def keys(self, carrier: textmap.CarrierT) -> List[str]:
        if carrier is None:
            return []
        return [key for (key, value) in carrier]


class KafkaContextSetter(textmap.Setter):
    def set(self, carrier: textmap.CarrierT, key: str, value: str) -> None:
        if carrier is None or key is None:
            return

        if value:
            value = value.encode()
        carrier.append((key, value))


def _get_argument(key, position, default_value, args, kwargs):
    if len(args) > position:
        return args[position]
    return kwargs.get(key, default_value)


def _get_topic(args, kwargs):
    """ extract topic from `send` method arguments in KafkaProducer class"""
    return _get_argument("topic", 0, "unknown", args, kwargs)


def _get_value(args, kwargs):
    """ extract value from `send` method arguments in KafkaProducer class"""
    return _get_argument("value", 1, None, args, kwargs)


def _get_key(args, kwargs):
    """ extract key from `send` method arguments in KafkaProducer class"""
    return _get_argument("key", 2, None, args, kwargs)


def _get_headers(args, kwargs):
    """ extract headers from `send` method arguments in KafkaProducer class"""
    return _get_argument("headers", 3, None, args, kwargs)


def _get_partition(instance, args, kwargs):
    """ extract partition `send` method arguments, using the `_partition` method in KafkaProducer class"""
    partition = _get_argument("partition", 4, None, args, kwargs)
    topic = _get_topic(args, kwargs)
    key = _get_key(args, kwargs)
    value = _get_value(args, kwargs)
    key_bytes = instance._serialize(instance.config['key_serializer'], topic, key)
    value_bytes = instance._serialize(instance.config['value_serializer'], topic, value)
    valid_types = (bytes, bytearray, memoryview, type(None))
    if type(key_bytes) not in valid_types or type(value_bytes) not in valid_types:
        return None
    try:
        return instance._partition(topic, partition, key, value, key_bytes, value_bytes)
    except Exception as err:
        _LOG.debug('Could not get partition', err)
        return None


def _create_producer_span(tracer, span_name, topic, partition, value, headers, bootstrap_servers):
    with tracer.start_as_current_span(span_name, kind=trace.SpanKind.PRODUCER) as span:
        _set_span_attributes(span, topic, partition, value, headers, bootstrap_servers)
        span.set_attribute(SpanAttributes.MESSAGING_OPERATION, 'send')
        inject(headers, context=set_span_in_context(span), setter=KafkaContextSetter())


def _create_consumer_span(tracer, span_name, topic, partition, value, headers, timestamp, bootstrap_servers):
    extracted_context = extract(headers, getter=KafkaContextGetter())
    span = tracer.start_span(span_name, context=extracted_context, kind=trace.SpanKind.CONSUMER)
    new_context = trace.set_span_in_context(span, extracted_context)
    token = attach(new_context)
    setattr(span, 'context_token', token)
    with trace.use_span(span):
        _set_span_attributes(span, topic, partition, value, headers, bootstrap_servers)
        span.set_attribute(SpanAttributes.MESSAGING_OPERATION, 'process')
        span.set_attribute('messaging.queue_time', round(time.time() * 1000 - timestamp)) if timestamp else None


def _serialize_payload(value):
    result = value
    value_type = type(value)
    if value_type == dict:
        result = json.dumps(value)
    elif value_type == bytes:
        result = value.decode()
    return result


def _serialize_headers(headers):
    if type(headers) == list:
        headers_dict = {}
        for headers_tuple in headers:
            if type(headers_tuple) == tuple and len(headers_tuple) == 2:
                value = headers_tuple[1].decode() if type(headers_tuple[1]) == bytes else headers_tuple[1]
                headers_dict[headers_tuple[0]] = value
        return json.dumps(headers_dict)
    return None


def _set_span_attributes(span, topic, partition, value, headers, bootstrap_servers):
    if span.is_recording():
        span.set_attribute(SpanAttributes.MESSAGING_SYSTEM, 'kafka')
        span.set_attribute(SpanAttributes.MESSAGING_PROTOCOL, 'kafka')
        span.set_attribute(SpanAttributes.MESSAGING_DESTINATION, topic) if topic else None
        payload = _serialize_payload(value)
        span.set_attribute(SPAN_ATTRIBUTES_MESSAGING_PAYLOAD, payload) if payload else None
        span.set_attribute(SpanAttributes.MESSAGING_KAFKA_PARTITION, partition) if partition is not None else None
        span.set_attribute(SpanAttributes.MESSAGING_URL, json.dumps(bootstrap_servers))
        serialized_headers = _serialize_headers(headers)
        span.set_attribute(SPAN_ATTRIBUTES_MESSAGING_KAFKA_HEADERS, serialized_headers) if serialized_headers else None


def _instrument(tracer: Tracer):
    def _end_current_consumer_span():
        current_span = trace.get_current_span()
        if current_span.is_recording() and current_span.name == CONSUMER_SPAN_NAME:
            context_token = getattr(current_span, 'context_token', None)
            detach(context_token) if context_token else None
            current_span.end()

    def _traced_send(func, instance, args, kwargs):
        try:
            span_name = PRODUCER_SPAN_NAME
            topic = _get_topic(args, kwargs)
            value = _get_value(args, kwargs)
            value_bytes = instance._serialize(instance.config['value_serializer'], topic, value)
            headers = _get_headers(args, kwargs)
            if headers is None:
                headers = []
                kwargs["headers"] = headers
            partition = _get_partition(instance, args, kwargs)
            bootstrap_servers = instance.config.get('bootstrap_servers')
            _create_producer_span(tracer, span_name, topic, partition, value_bytes, headers, bootstrap_servers)
        except Exception as error:
            _LOG.debug('kafka send instrumentation error: %s.', error)

        return func(*args, **kwargs)

    def _traced_next(func, instance, args, kwargs):
        try:
            _end_current_consumer_span()
        except Exception as error:
            _LOG.debug('kafka __next__ instrumentation error: %s.', error)

        bootstrap_servers = instance.config.get('bootstrap_servers')
        record = func(*args, **kwargs)

        if record:
            try:
                _create_consumer_span(tracer, CONSUMER_SPAN_NAME, record.topic, record.partition,
                                      record.value, record.headers, record.timestamp, bootstrap_servers)
            except Exception as error:
                _LOG.debug('kafka __next__ instrumentation error: %s.', error)

        return record

    def _traced_commit(func, instance, args, kwargs):
        try:
            _end_current_consumer_span()
        except Exception as error:
            _LOG.debug('kafka commit instrumentation error.', error)

        return func(*args, **kwargs)

    wrap_function_wrapper("kafka", "KafkaProducer.send", _traced_send)
    wrap_function_wrapper("kafka", "KafkaConsumer.__next__", _traced_next)
    wrap_function_wrapper("kafka", "KafkaConsumer.commit", _traced_commit)


def _is_supported():
    # Older, unsupported versions of kafka don't have this property
    return hasattr(kafka, '__version__')


class KafkaInstrumentor(BaseInstrumentor):
    """An instrumentor for kafka module
    See `BaseInstrumentor`
    """

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        if not _is_supported():
            return

        tracer_provider = kwargs.get("tracer_provider")
        tracer = trace.get_tracer(
            'opentelemetry.instrumentation.kafka_python', __version__, tracer_provider=tracer_provider
        )

        _instrument(tracer)

    def _uninstrument(self, **kwargs):
        if not _is_supported():
            return

        unwrap(kafka.KafkaProducer, "send")
        unwrap(kafka.KafkaConsumer, "__next__")
        unwrap(kafka.KafkaConsumer, "commit")
