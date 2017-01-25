class AsyncResponse(object):
    """
    Describes the result of a call.
    """
    def __init__(self, key , success , result , error):
        """
        The constructor
        :param key (str): the random key used to associate AsyncCall and AsyncResponse objects
        :param success (bool):
        :param result (object): indicates if execution of the call was successful
        :param error (exception): exception that occurred during execution of the call
        """
        self.key = key
        self.success = success
        self.result = result
        self.error = error
