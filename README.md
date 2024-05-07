# pytest-sample-argvalues
A utility function to help choose a random sample from your argvalues in pytest

## Install
```python
pip install pytest-sample-argvalues
```

## Why would I need this?

One of the cool features of pytest is that you can stack multiple instances of `pytest.mark.parametrize`, to get all combinations of multiple parametrized arguments. See the [docs](https://docs.pytest.org/en/7.1.x/how-to/parametrize.html) for full details. For instance:
```python
import pytest


@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    pass

# This will run the test with the arguments set to x=0/y=2, x=1/y=2, x=0/y=3, and x=1/y=3 exhausting parameters in the order of the decorators.
```

However, it quickly becomes apparent that this product of parameters can grow vey quickly, leading to too many tests...

## Example Usage

This package present an easy method of taking a random sample of your multiple parametrized arguments. This is useful if you don't have time to run all of your tests (or there are simply too many!), and want to check a random sample of them, to find any potential bugs. For instance,

```python
import pytest
from pytest_argvalues_sample import pytest_argvalues_sample

MAX_TESTS = 1_000
SAMPLE_FRACTION = 0.000001
PARAMS = {
    "a": list(range(1000)),
    "b": list(range(1000)),
    "c": list(range(1000)),
}

@pytest.mark.parametrize(
    "a,b,c",
    argvalues=pytest_argvalues_sample(PARAMS, SAMPLE_FRACTION, MAX_TESTS)
)
def test_param_sample(a: int, b: int, c: int):
    assert a + b + c <= 2997
```

Instead of attempting to run `1000**3` pytests, this will run `(1000**3)*0.000001=1000` pytests.
