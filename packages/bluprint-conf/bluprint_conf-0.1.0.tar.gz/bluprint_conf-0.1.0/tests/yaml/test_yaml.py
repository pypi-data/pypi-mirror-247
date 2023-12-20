"""Test YAML manipulation."""

from bluprint_conf import add_prefix_to_nested_config, load_config_yaml


def test_load_data_yaml():
    actual_test_config = load_config_yaml('tests/yaml/fixtures/test.yaml')
    actual_test_config = add_prefix_to_nested_config(
        actual_test_config,
        prefix='/xyz/',
    )
    expected_test_config = load_config_yaml(
        'tests/yaml/snapshots/prefixed_test.yaml',
    )
    assert dict(actual_test_config) == dict(expected_test_config)
