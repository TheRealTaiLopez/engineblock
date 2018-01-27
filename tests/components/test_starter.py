import pytest

from engineblock.timing_constants import StarterSignals
from tests.components.component_fixtures import dummy_starter


@pytest.mark.parametrize("test_function, is_started, expected", [
    ("start", True, StarterSignals.START),
    ("start", False, StarterSignals.START),
    ("stop", True, StarterSignals.STOP),
    ("stop", False, StarterSignals.STOP),
])
def test_status(test_function, is_started, expected):
    test_starter, _ = dummy_starter()
    test_starter.status = StarterSignals.START if is_started else StarterSignals.STOP
    getattr(test_starter, test_function)()
    assert test_starter.status == expected
