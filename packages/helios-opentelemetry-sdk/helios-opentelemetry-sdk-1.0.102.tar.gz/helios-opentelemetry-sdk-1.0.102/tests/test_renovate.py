import json


def test_renovate():
    renovate = json.loads(open('renovate.json').read())['packageRules'][1]['matchPackageNames']
    requirements = [x.split("==")[0] for x in open('requirements.txt').read().strip().split('\n') if 'opentelemetry' in x and not x.startswith('#')]
    assert sorted(renovate) == sorted(requirements)
