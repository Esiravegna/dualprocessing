import time


class HowLong(object):
    """
    Just a very simple wrapper of timer in order to get the time elapsed by a task
    """
    def __init__(self):
        """
        Builds the timers
        """
        self.start = time.time()

    def timeit(self):
        """
        Returns the elapsed time since the object creation
        :return: the time
        """
        return self.start - time.time()
