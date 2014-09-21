"""This module contain only a single class: ThreadList

See help(ThreadList) for more informations
"""

import time
import threading

__author__  = 'Dorian Fevrier <fevrier.dorian@yahoo.fr>'

__all__ = ["ThreadList",
           "StartingError",
           "TimeoutError"]

class ExecutionOrderError(Exception):
    """Raised when ThreadList methods are called in an inconsistant order"""
    def __init__(self, msg):
        Exception.__init__(self, msg)

class TimeoutError(Exception):
    """Raised when ThreadList reach timeout"""
    def __init__(self, msg):
        Exception.__init__(self, msg)

class ThreadList(list):
    """An extended Python list to handle (and limit) thread executions

    When you run many threading.Thread() instances, you can reach the maximum
    number of thread your system can support. This special list provide some
    controls on how threads are started.

    The way threads are handles by this list is time based. This is efficient
    for slow threads (slower than 0.1 sec) but can be less efficient on
    multiple very fast threads.

    Args:
      Same as a build in Python list

    Properties:
      max_count (int)           : The maximum number of threads that will run
                                  together (default: -1 meaning no limit).
      total_timeout (int, float): The maximum time (in seconds) the thread loop
                                  will run before raise a TimeoutError
                                  exception (default: -1 meaning no limit).
      wait_time (int, float)    : The time the loop wait (in seconds) before
                                  check threads status again. More the threads
                                  are fast, less this value should be
                                  (default: 0.5).
      is_running (readonly)     : Return if the thread list is running.

    Methods:
      run()   : Hang your script execution, start the thread list and terminate
                them. This is the prefered way to handle ThreadList.
      start() : Start every threads in the list. You are supposed to call
                join() to terminate the thread list manually.
      join()  : Hang until every thread of the list is terminated. You should
                call this after start().

    Examples:
      >>> import threading
      >>> from threadlist import ThreadList
      >>> # The prefered way using run()
      >>> threads = ThreadList()
      >>> for _ in xrange(10):
      ...     thread = threading.Thread()
      ...     threads.append(thread)
      >>> threads.max_count = 4
      >>> threads.total_timeout = 15
      >>> threads.run()

      >>> import threading
      >>> from threadlist import ThreadList
      >>> # The start/join way
      >>> threads = ThreadList()
      >>> for _ in xrange(10):
      ...     thread = threading.Thread()
      ...     threads.append(thread)
      >>> threads.start()
      >>> # Execute your own code here...
      >>> threads.join()
    """

    def __init__(self, *args):
        """Init the class the same way than the builtin Python list"""
        list.__init__(self, *args)
        self.__max_count     = -1
        self.__total_timeout = -1
        self.__wait_time     = 0.5
        self.__running       = False
        self.__start_time    = None

    @property
    def max_count(self):
        """The maximum number of threads that will run together"""
        return self.__max_count

    @max_count.setter
    def max_count(self, value):
        if self.__running :
            msg = ("ThreadList running, can not change property max_count. "
                   "Please run joint()" )
            raise ExecutionOrderError(msg)
        self.__max_count = value

    @property
    def total_timeout(self):
        """The maximum time (in seconds) the thread loop will run before raise
        a TimeoutError exception"""
        return self.__total_timeout

    @total_timeout.setter
    def total_timeout(self, value):
        if self.__running :
            msg = ("ThreadList running, can not change property total_timeout. "
                   "Please run joint()" )
            raise ExecutionOrderError(msg)
        self.__total_timeout = value

    @property
    def wait_time(self):
        """The time the loop wait (in seconds) before check threads status
        again"""
        return self.__wait_time

    @wait_time.setter
    def wait_time(self, value):
        if self.__running :
            msg = ("ThreadList running, can not change property wait_time. "
                   "Please run joint()" )
            raise ExecutionOrderError(msg)
        self.__wait_time = value

    @property
    def is_running(self):
        """Return if the thread list is running."""
        return self.__running

    def start(self):
        """StartCall start() method on every threads in the list"""

        if self.__running:
            msg = "ThreadList already running, please call join()"
            raise ExecutionOrderError(msg)

        self.__running    = True
        self.__start_time = time.time()
        pending_threads   = list(self)

        while pending_threads :

            self.__check_total_timeout()

            time.sleep(self.__wait_time)

            # Compute the number of possible threads to launch
            if self.__max_count > 0 :
                free_slot_count = self.__max_count - threading.active_count()
                if free_slot_count <= 0 : continue
            else :
                free_slot_count = len(pending_threads)

            # Ensure we will not start more threads than we have
            if free_slot_count > len(pending_threads):
                free_slot_count = len(pending_threads)

            for _ in xrange(free_slot_count):
                pending_threads.pop().start()

    def join(self):
        """Call join() method on every threads in the list"""
        if not self.__running :
            msg = "ThreadList not running, please call start()"
            raise ExecutionOrderError(msg)
        for thread in self:
            self.__check_total_timeout()
            thread.join()
        self.__running = False

    def __check_total_timeout(self):
        """Check the loop doesn't reach the setted total timeout"""
        if self.__total_timeout > 0:
            elapsed = time.time() - self.__start_time
            if elapsed > self.__total_timeout:
                msg = "Timeout (%ss) reached: %ss" % (self.__total_timeout,
                                                      elapsed)
                raise TimeoutError(msg)

    def run(self):
        """Start the thread list execution  and wait until they are all
        finished"""
        self.start()
        self.join()

if __name__ == "__main__":

    # a thread class that print itself...
    class MyThread(threading.Thread):
        def run(self):
            print self

    threads = ThreadList()
    for _ in xrange(10):
        thread = MyThread()
        threads.append(thread)
    threads.max_count = 4
    threads.wait_time = 0.2
    threads.total_timeout = 15
    threads.run()

