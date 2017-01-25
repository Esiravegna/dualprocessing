from dualprocessing.async_response import AsyncResponse


def answer():
    return 42


def test_async_call():
    response = AsyncResponse('this_is_a_key', True, 42, False)
    assert response.key == 'this_is_a_key'
    assert not response.error
    assert response.result == 42
    assert response.success

