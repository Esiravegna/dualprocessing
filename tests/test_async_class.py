from dualprocessing.async_call import AsyncCall


def answer():
    return 42


def test_async_call():
    kwargs = {"arg3": 3, "arg2": "two"}
    a = AsyncCall(answer, (), **kwargs)
    assert a.target_method() == 42
    assert len(a.kwargs) == 2

