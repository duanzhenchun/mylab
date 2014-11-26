import threading
import time

MAX_JOBS=10

class Job(object):
    def run(self):
        print 'job run'

class Manager(object):
    def __init__(self, nworks=4):
        self.jobs = []
        self.cond = threading.Condition()   #lock inside
        self.start_works(nworks)

    def start_works(self, num):
        self.on = True
        for i in range(num):
            th = threading.Thread(target=self.work, args=(i,))
            th.start() 

    def work(self, i):
        print 'thread: %s started' %i
        while self.on:
            self.cond.acquire()
            #releases the underlying lock, and then blocks until it is awakened by a notify() or notifyAll()
            self.cond.wait()
            job=None
            if len(self.jobs)>0:
                job = self.jobs.pop(0)
            self.cond.release()
            if job:
                job.run()

    def add(self, job):
        self.cond.acquire()
        if len(self.jobs)<MAX_JOBS:
            self.jobs.append(job)
        self.cond.notify()
        self.cond.release()
        
    def stop(self):
        self.cond.acquire()
        self.on=False
        self.cond.notifyAll()
        self.cond.release()

    def set_works(self, n):
        self.stop()
        self.start_works(n)


def test():
    mgr=Manager()
    while True:
        s = raw_input('add/stop/set_n jobs?')
        if s.startswith('a'):
            mgr.add(Job())
        elif s.startswith('s'):
            break 
        else:
            try:
                mgr.set_works(int(s))
            except:
                break
    mgr.stop()

test()
