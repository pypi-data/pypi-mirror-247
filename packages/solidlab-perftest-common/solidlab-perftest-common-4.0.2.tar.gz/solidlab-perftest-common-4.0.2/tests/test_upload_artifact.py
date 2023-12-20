import pytest

from solidlab_perftest_common.upload_artifact import validate_artifact_endpoint


def test_validate_artifact_endpoint_ok_1a():
    actual = validate_artifact_endpoint(
        "https://example.com/api/v1/experiment/1/artifact/"
    )
    expected = "https://example.com/api/v1/experiment/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_1b():
    actual = validate_artifact_endpoint(
        "https://example.com/api/v1/experiment/1/artifact"
    )
    expected = "https://example.com/api/v1/experiment/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_1c():
    actual = validate_artifact_endpoint("https://example.com/api/v1/experiment/1/")
    expected = "https://example.com/api/v1/experiment/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_1d():
    actual = validate_artifact_endpoint("https://example.com/api/v1/experiment/1")
    expected = "https://example.com/api/v1/experiment/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_1e():
    actual = validate_artifact_endpoint(
        "http://example.com/api/v1/experiment/1/artifact/"
    )
    expected = "http://example.com/api/v1/experiment/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_2a():
    actual = validate_artifact_endpoint(
        "https://example.com/api/v1/testenv/1/artifact/"
    )
    expected = "https://example.com/api/v1/testenv/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_2b():
    actual = validate_artifact_endpoint("https://example.com/api/v1/testenv/1/artifact")
    expected = "https://example.com/api/v1/testenv/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_2c():
    actual = validate_artifact_endpoint("https://example.com/api/v1/testenv/1/")
    expected = "https://example.com/api/v1/testenv/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_2d():
    actual = validate_artifact_endpoint("https://example.com/api/v1/testenv/1")
    expected = "https://example.com/api/v1/testenv/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_22():
    actual = validate_artifact_endpoint("http://example.com/api/v1/testenv/1/artifact/")
    expected = "http://example.com/api/v1/testenv/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_3a():
    actual = validate_artifact_endpoint(
        "https://example.com/api/v1/perftest/1/artifact/"
    )
    expected = "https://example.com/api/v1/perftest/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_3b():
    actual = validate_artifact_endpoint(
        "https://example.com/api/v1/perftest/1/artifact"
    )
    expected = "https://example.com/api/v1/perftest/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_3c():
    actual = validate_artifact_endpoint("https://example.com/api/v1/perftest/1/")
    expected = "https://example.com/api/v1/perftest/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_3d():
    actual = validate_artifact_endpoint("https://example.com/api/v1/perftest/1")
    expected = "https://example.com/api/v1/perftest/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_ok_3e():
    actual = validate_artifact_endpoint(
        "http://example.com/api/v1/perftest/1/artifact/"
    )
    expected = "http://example.com/api/v1/perftest/1/artifact"
    assert actual == expected


def test_validate_artifact_endpoint_fail_1():
    with pytest.raises(ValueError):
        validate_artifact_endpoint("dummy")


def test_validate_artifact_endpoint_fail_2():
    with pytest.raises(ValueError):
        validate_artifact_endpoint("https://example.com/api/v1/exp/1/artifact/")


def test_validate_artifact_endpoint_fail_3():
    with pytest.raises(ValueError):
        validate_artifact_endpoint("https://example.com/api/v1/experiment/")
