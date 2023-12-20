from json import load
from os.path import dirname, realpath
from pathlib import Path

from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.trace import SpanContext

from helios.base.span_attribute_dropper import SpanAttributeDropper

TestData = {
    'original_span': dict,
    'span_after_drop': dict
}


def get_test_data() -> TestData:
    test_data_file_name = 'span-attribute-dropper.json'
    with open(Path(dirname(realpath(__file__)), 'resources', test_data_file_name)) as fp:
        test_data = load(fp)

    return test_data


def test_metadata_only_mode():
    test_data = get_test_data()
    original_span = test_data['original_span']
    span_after_drop = test_data['span_after_drop']
    ctx = SpanContext(1234, 5678, False)
    span = ReadableSpan('', attributes=original_span['attributes'], context=ctx)

    span_attribute_dropper = SpanAttributeDropper()
    span_attribute_dropper.drop_non_metadata_attributes(span)

    assert {key: value for key, value in span.attributes.items()} == span_after_drop['attributes']


def test_metadata_only_mode_with_aws_span():
    test_data = get_test_data()
    original_aws_span = test_data['original_aws_span']
    aws_span_after_drop = test_data['aws_span_after_drop']
    ctx = SpanContext(1234, 5678, False)
    span = ReadableSpan('', attributes=original_aws_span['attributes'], context=ctx)

    span_attribute_dropper = SpanAttributeDropper()
    span_attribute_dropper.drop_non_metadata_attributes(span)

    assert {key: value for key, value in span.attributes.items()} == aws_span_after_drop['attributes']
