from uuid import uuid4


class AsyncCall(object):
    """
    Describes a call to the pipeline.
    """

    def __init__(self, targetmethod, *args, **kwargs):
        """
        :param targetMethod (str): the name of the method to call (must be a method of the object returned by the function that you pass to the Broker constructor)
        :param args: Variable length argument list. (arguments of the target method)
        :param kwargs:
        """

        self.target_method = targetmethod
        self.key = str(uuid4())
        self.args = args
        self.kwargs = kwargs
