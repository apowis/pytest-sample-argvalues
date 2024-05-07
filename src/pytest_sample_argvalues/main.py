"""
Contains the code for the pytest_sample_argvalues package.
"""

from math import prod
from typing import Any, Generator, Optional

from iteration_utilities import random_product

try:
    from itertools import batched, islice
except ImportError:  # itertools.batched is new in Python 3.12
    from itertools import islice

    def batched(iterable, n) -> Generator[tuple, Any, None]:
        """Batch elements of an iterable."""
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(islice(it, n)):
            yield batch


def pytest_sample_argvalues(
    params: dict[str, list], sample_fraction: float, max_tests: Optional[int] = None
) -> Generator[tuple, Any, None]:
    """
    Given a potentially large number of paramtrized argvalues in pytest,
    this generates a sample of them.
    Example Usage:
        MAX_TESTS = 1_000
        SAMPLE_FRACTION = 0.000001
        PARAMS = {
            "a": list(range(1000)),
            "b": list(range(1000)),
            "c": list(range(1000)),
        }

        @pytest.mark.parametrize(
            "a,b,c",
            argvalues=pytest_sample_argvalues(PARAMS, SAMPLE_FRACTION, MAX_TESTS)
        )
        def test_param_sample(a: int, b: int, c: int):
            assert a + b + c <= 2997

    :param params: dictionary of parameters
    :param sample_fraction: fraction of the total number of tests to generate
    :param max_tests: maximum number of tests to generate,
        if the sample size is too large, raise an ValueError
    :return: generator of test parameters
    """
    sample_size = int(
        prod([len(value) for value in params.values()]) * sample_fraction
    )
    if max_tests and sample_size > max_tests:
        raise ValueError(
            f"Sample size too large - {sample_size=}. Use smaller sample_fraction."
        )

    yield from batched(
        random_product(*params.values(), repeat=sample_size), len(params)
    )
