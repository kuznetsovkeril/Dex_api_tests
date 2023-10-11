import time
import pytest


@pytest.fixture(scope="function")
def wait_between_tests():
    delay = 20
    time.sleep(delay)