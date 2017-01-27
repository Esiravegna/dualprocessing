from __future__ import absolute_import
from __future__ import print_function
from concurrent import futures
import logging
from multiprocessing.connection import Pipe
from multiprocessing import Process
from time import sleep
from sys import exc_info
from .async_response import AsyncResponse

__version__ = "0.2.3"


logger = logging.getLogger(__name__)


class Broker(object):
    """
    Handles scheduling and running of computations on a second process.
    """

    def __init__(self, process_constructor, *pc_args, **pc_kwargs):
        """
        Starts a second thread for calling methods on the instance created through processorConstructor.
        :param process_constructor (function): function that returns an instance of the computation pipeline
        :param pc_args: Variable length argument list. (arguments of processor constructor)
        :param pc_kwargs:  Arbitrary keyword arguments (of the processor constructor)
        """
        self.finished_tasks = {}
        self.running_tasks = []
        child_end, self.__parent_end__ = Pipe()
        self.__computational_process__ = Process(target=self.__start__,
                                                 args=(child_end, process_constructor, pc_args, pc_kwargs),
                                                 name="ComputationProcess")
        self.__computational_process__.start()
        self.thread_executor = futures.ThreadPoolExecutor(256)
        self.thread_executor.submit(self.__receive__)
        return

    @classmethod
    def __start__(cls, pipe_end, processor_constructor, pc_args, pc_kwargs):
        """
        Instantiates the process_constructor and executes a call on such instance.
        Listens for incoming calls through the pipe.
        Sends return values of executed calls back through the pipe.

        :param pipe_end: (multiprocessing.connection.Pipe) child end of the pipe connection to the broker process
        :param processor_constructor (function): the computate pipeline constructor
        :param pc_args (list): an *args for the processor_constructor
        :param pc_kwargs (dict): a **kwargs for the processor_constructor
        """
        logging.info("Broker: initializing...")
        # we're now on the second process, so we can create the processor
        processor = processor_constructor(*pc_args, **pc_kwargs)
        logging.info("Broker: initialization completed")
        # endlessly loop
        while True:
            # get input key
            call, = pipe_end.recv()
            # process input synchronously
            logging.info("{0} processing".format(call.key))
            # execute the said method on the processor
            response = None
            try:
                returned = processor.__getattribute__(call.target_method)(*call.args, **call.kwargs)
                response = AsyncResponse(call.key, True, returned, None)
            except Exception as e:
                logger.exception(e)
                response = AsyncResponse(call.key, False, None, exc_info()[1])
            pipe_end.send((response,))
            # continue looping

    def submit_call(self, call):
        """
        Submits a call
        :param call: (AsyncCall class) the call to be scheduled
        :return: the key parameter as per that class, for a new one.
        """
        logging.info("{0} scheduled {1}".format(call.key, call.target_method))
        # add the key to the queue
        self.__parent_end__.send((call,))
        self.running_tasks.append(call.key)
        return call.key

    def submit_call_async(self, call):
        """
        (asynchronous) Submits a call and yields the result.
        Example:

        @trollius.coroutine
        def myfunc():
            call = broker.AsyncCall("uppercase", text="blabla")
            asyncResponse = yield a_broker.submit_call_async(call)
            print(asyncResponse.sucess)
            print(asyncResponse.result)
        :param call: (AsyncCall class) the call to be scheduled
        :return: a generator yienlding an AsyncResponse. See that class for details
        """
        self.submit_call(call)
        return self.get_result_async(call.key)

    def get_result_async(self, key):
        """
        (asynchronous) Spawns a thread to wait for completion of a running call.
        Examples
        --------
        @trollius.coroutine
        def myfunc():
            call = broker.AsyncCall("uppercase", text="blabla")
            a_broker.submitCall(call)
            asyncResponse = yield compuBroker.getResultAsync(call.key)
            print(asyncResponse.sucess)
            print(asyncResponse.result)

        :param key: (str) the key to be polled asynchronously
        :return a thread execution future, as per ThreadPoolExecutor
        """
        return self.thread_executor.submit(self.get_result, key)

    def get_result(self, key):
        """
        (blocking) Waits until the key is not present in RunningTasks.

        :param key: (str) the key to be polled
        :return (AsyncResponse || None)
        """
        result = None
        while key in self.running_tasks:
            sleep(0.05)
        if key in self.finished_tasks:
            result = self.finished_tasks.pop(key)
        return result

    def __receive__(self):
        """
        Listens in the background waiting to tasks to be finished
        """
        while True:
            sleep(0.005)
            # receive all computations that have finished
            while self.__parent_end__.poll():
                response, = self.__parent_end__.recv()
                self.finished_tasks[response.key] = response
                self.running_tasks.remove(response.key)
                if not response.Success:
                    logging.warning("{0} failed: {1}".format(response.key, response.Error))
                else:
                    logging.info("{0} completed".format(response.key))
