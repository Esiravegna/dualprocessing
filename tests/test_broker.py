import pytest
from time import sleep
from dualprocessing import Broker, AsyncCall
import trollius

class mocked_compute_pipeline(object):
    """
    A mocked compute pipeline
    """

    def __init__(self):
        """
        Let simulate a slow to create object, 10 seconds
        """
        sleep(10)

    def compute(self, *args, **kwargs):
        sleep(2)
        return 42


@pytest.fixture()
def get_pipe():
    return mocked_compute_pipeline


@trollius.coroutine
def test_the_default_process():
    broker = Broker(mocked_compute_pipeline)
    call_1 = yield broker.submit_call(AsyncCall("compute"))
    call_2 = yield broker.submit_call_async(AsyncCall("compute"))
    assert call_1.success
    assert call_1.result == 42
    assert call_2.success
    assert call_2.result == 42