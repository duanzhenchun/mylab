import gearman
import json
import time

Servers=['localhost:4730',]
workfn='work_api'


def work_use():
    def taskfn(worker, job):
        #print worker.worker_client_id 
        time.sleep(1)
        print job.data
        data = json.loads(job.data)
        res = json.dumps(data.values())
        return res 

    gw = gearman.GearmanWorker(Servers)
    gw.set_client_id('work_0')   #optional
    gw.register_task(workfn, taskfn)

    # Enter our work loop
    gw.work()


def cli_use():
    cli = gearman.GearmanClient(Servers)
#    data={'a':1,'b':2}
#        req = cli.submit_job(workfn, json.dumps(data))
# async
    lst=[]
    for i in range(10):
        lst.append(dict(task=workfn, data=str(i)))
    reqs=cli.submit_multiple_jobs(lst, wait_until_complete=False)
    res = cli.wait_until_jobs_completed(reqs, poll_timeout=5.0)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        sys.exit("""
Usage:
    %s -w/-c""" %sys.argv[0])
    if sys.argv[1] == '-w':
        work_use()
    else:
        cli_use()
