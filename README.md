threadlist
==========

A thread loop "limiter" module for Python

ThreadList
----------

An extended builtin list to handle (and limit) Python threads execution.

When you run many slow threading.Thread() instances, you can reach the maximum number of thread your system can support. This special list provide some controls on how threads are started.

The way threads are handles by this list is time based. This is efficient for slow threads (slower than 0.1 sec) but can be less efficient on multiple very fast threads.

```python
import threading
from threadlist import ThreadList

threads = ThreadList()
for i in xrange(10):
    thread = threading.Thread()
    threads.append(thread)
threads.max_count = 4
threads.timeout = 15
threads.run()
```
