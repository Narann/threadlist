threadlist
==========

A thread loop "limiter" module for Python.

More details using:

```python
import threadlist
help(threadlist)
```


ThreadList
----------

An extended Python list to handle (and limit) thread executions.

When you run many slow threading.Thread() instances, you can reach the maximum number of thread your system can support. This special list provide some controls on how threads are started.

The way threads are handles by this list is time based. This is efficient for slow threads (slower than 0.1 sec) but can be less efficient on multiple very fast threads.

```python
import threading
from threadlist import ThreadList, TimeoutError

threads = ThreadList()
for _ in xrange(10):
    thread = threading.Thread()
    threads.append(thread)
threads.max_count = 4
threads.total_timeout = 15
try:
    threads.run() # wait until every thread is terminated
except TimeoutError:
    print "Threads Timeout reached!"
```

A typical big images conversion example:

```python
import threading, multiprocessing
from threadlist import ThreadList

image_paths # a huge list of image file to convert

threads = ThreadList()
for image_path in image_paths:
    thread = SlowConversionThread(image_path)
    threads.append(thread)
threads.max_count = multiprocessing.cpu_count()
threads.start()
# continue your script here...
threads.join()
```
