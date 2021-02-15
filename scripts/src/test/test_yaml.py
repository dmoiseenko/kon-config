import pytest
import os

from src.common.yaml import (
    update_yaml_file,
    create_yaml_file_by_dictionary,
    read_yaml_file_to_dictionary,
    get_yaml_file_field_value
)


test_dictionary = dict(
    A="foo",
    B=dict(
        C="bar",
        D="baz",
    ),
)
test_yaml_file_path = "test.yaml"


@pytest.fixture
def create_yaml_file():
    create_yaml_file_by_dictionary(test_yaml_file_path, test_dictionary)
    yield
    os.remove(test_yaml_file_path)


def test_update_yaml_file(create_yaml_file):
    update_yaml_file(test_yaml_file_path, "B.C", "test")
    dictionary = read_yaml_file_to_dictionary(test_yaml_file_path)

    assert dictionary["B"]["C"] == "test"


def test_get_yaml_file_field_value(create_yaml_file):
    value = get_yaml_file_field_value(test_yaml_file_path, "B.C")

    assert value == "bar"
