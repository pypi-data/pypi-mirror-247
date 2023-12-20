from json import load
from os.path import dirname, realpath
from pathlib import Path
from typing import List, Optional
from timeit import default_timer as timer
import copy

from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.trace import SpanContext

from helios.base.data_obfuscator import DataObfuscator, DataObfuscatorConfiguration
from helios.base.data_obfuscator.base_data_obfuscator import Mode

ResourceCollection = {
    'span': dict,
    'obfuscated_span_allowlist': dict,
    'obfuscated_span_blocklist': dict
}
TestData = {
    'data_obfuscation_config': dict,
    'resource_collections': List[type(ResourceCollection)]
}

JSON_ATTRIBUTES = {
    'default': ['http.request.body', 'db.statement', 'messaging.payload'],
    'redis': ['db.query_result'],
    'stress-test': ['db.query_result']
}


def obfuscate_and_assert_resource_collection(
        data_obfuscator: DataObfuscator,
        mode: Mode,
        resource_collection: ResourceCollection
):
    # Initialize spans.
    span = resource_collection['span']
    ctx = SpanContext(1234, 5678, False)
    span = ReadableSpan('', attributes=span['attributes'], context=ctx)
    obfuscated_span = resource_collection[f'obfuscated_span_{mode}']

    # Act and assert.
    data_obfuscator.obfuscate_data(span)
    assert {key: value for key, value in span.attributes.items()} == obfuscated_span['attributes']


def get_test_data(obfuscator_name: Optional[str] = 'default') -> TestData:
    test_data_file_name = f'{obfuscator_name}-data-obfuscation.json'
    with open(Path(dirname(realpath(__file__)), 'resources', test_data_file_name)) as fp:
        test_data = load(fp)

    for resource_collection in test_data['resource_collections']:
        for resourceName in resource_collection.keys():
            attributes = resource_collection[resourceName]['attributes']

            for attribute in JSON_ATTRIBUTES[obfuscator_name]:
                if attribute in attributes:
                    attributes[attribute] = attributes[attribute]

    return test_data


def test_data_obfuscation_in_allowlist_mode():
    # Get resources.
    test_data = get_test_data()
    data_obfuscation_config = test_data['data_obfuscation_config']
    resource_collections = test_data['resource_collections']

    # Initialize data obfuscator.
    allowlist_data_obfuscator = DataObfuscator(DataObfuscatorConfiguration(
        hmac_key=data_obfuscation_config['hmacKey'],
        http_headers_mode='allowlist',
        http_headers_rules=data_obfuscation_config['httpHeadersRules'],
        mode='allowlist',
        rules=data_obfuscation_config['rules']
    ))

    # Test resource collections.
    for resource_collection in resource_collections:
        obfuscate_and_assert_resource_collection(allowlist_data_obfuscator, 'allowlist', resource_collection)


def test_data_obfuscation_in_blocklist_mode():
    # Get resources.
    test_data = get_test_data()
    data_obfuscation_config = test_data['data_obfuscation_config']
    resource_collections = test_data['resource_collections']

    # Initialize data obfuscator.
    allowlist_data_obfuscator = DataObfuscator(DataObfuscatorConfiguration(
        hmac_key=data_obfuscation_config['hmacKey'],
        http_headers_mode='blocklist',
        http_headers_rules=data_obfuscation_config['httpHeadersRules'],
        mode='blocklist',
        rules=data_obfuscation_config['rules']
    ))

    # Test resource collections.
    for resource_collection in resource_collections:
        obfuscate_and_assert_resource_collection(allowlist_data_obfuscator, 'blocklist', resource_collection)


def test_data_obfuscation_in_allowlist_mode_for_redis():
    # Get resources.
    test_data = get_test_data('redis')
    data_obfuscation_config = test_data['data_obfuscation_config']
    resource_collections = test_data['resource_collections']

    # Initialize data obfuscators.
    allowlist_data_obfuscator = DataObfuscator(DataObfuscatorConfiguration(
        hmac_key=data_obfuscation_config['hmacKey'],
        http_headers_mode=None,
        http_headers_rules=None,
        mode='allowlist',
        rules=data_obfuscation_config['rules']
    ))

    # Test resource collections.
    for resource_collection in resource_collections:
        obfuscate_and_assert_resource_collection(allowlist_data_obfuscator, 'allowlist', resource_collection)


def test_data_obfuscation_in_blocklist_mode_for_redis():
    # Get resources.
    test_data = get_test_data('redis')
    data_obfuscation_config = test_data['data_obfuscation_config']
    resource_collections = test_data['resource_collections']

    # Initialize data obfuscators.
    blocklist_data_obfuscator = DataObfuscator(DataObfuscatorConfiguration(
        hmac_key=data_obfuscation_config['hmacKey'],
        http_headers_mode=None,
        http_headers_rules=None,
        mode='blocklist',
        rules=data_obfuscation_config['rules']
    ))

    # Test resource collections.
    for resource_collection in resource_collections:
        obfuscate_and_assert_resource_collection(blocklist_data_obfuscator, 'blocklist', resource_collection)


def test_data_obfuscation_in_blocklist_mode_for_redis_6over6():
    # Get resources.
    test_data = get_test_data('stress-test')
    data_obfuscation_config = test_data['data_obfuscation_config']
    resource_collections = test_data['resource_collections']

    # Initialize data obfuscators.
    blocklist_data_obfuscator = DataObfuscator(DataObfuscatorConfiguration(
        hmac_key=data_obfuscation_config['hmacKey'],
        http_headers_mode=None,
        http_headers_rules=None,
        mode='blocklist',
        rules=data_obfuscation_config['rules']
    ))
    for resource_collection in resource_collections:
        start = timer()
        for i in range(100):
            span_to_obfuscate = copy.deepcopy(resource_collection)
            obfuscate_and_assert_resource_collection(blocklist_data_obfuscator, 'blocklist',
                                                     span_to_obfuscate)
        end = timer()
        assert ((end - start) < 1.5)
