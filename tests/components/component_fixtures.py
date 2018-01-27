"""
This file contains fixtures to create component Object for testing.
"""
import pytest

from multiprocessing import Pipe

from engineblock.components import Starter


@pytest.fixture()
def dummy_starter():
    """
    This fixture simply returns a Starter object and the child pipe that it would communicate to.
    """
    test_pipe, receiving_end = Pipe()
    return Starter(test_pipe), receiving_end
