"""
Test the `pytest_sample_argvalues` function.
"""

import pytest
from pytest_sample_argvalues import pytest_sample_argvalues


MAX_TESTS = 1_000
SAMPLE_FRACTION = 0.000001
PARAMS = {
    "a": list(range(1000)),
    "b": list(range(1000)),
    "c": list(range(1000)),
}


def test_pytest_sample_argvalues_len():
    """
    Test the length of the generated sample.
    """
    assert (
        len(list(pytest_sample_argvalues(PARAMS, SAMPLE_FRACTION, MAX_TESTS))) == 1000
    )


@pytest.mark.parametrize(
    "a,b,c", argvalues=pytest_sample_argvalues(PARAMS, SAMPLE_FRACTION, MAX_TESTS)
)
def test_param_sample(a: int, b: int, c: int):
    """
    Test the sum of the three parameters using pytest_sample_argvalues.
    """
    assert a + b + c <= 2997
