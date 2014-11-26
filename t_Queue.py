from Queue import Queue
from threading import Thread

#ref: https://docs.python.org/2/library/queue.html

def source():
    return range(10)

def do_work(i):
    print i

def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

q = Queue(5)
for i in range(4):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in source():
    q.put(item)

q.join()       # block until all tasks are done
