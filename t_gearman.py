import gearman
import json

Servers=['localhost:4730',]
workfn='work_api'


def work_use():
    def taskfn(worker, job):
        #print worker.worker_client_id 
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
    data={'a':1,'b':2}
    req = cli.submit_job(workfn, json.dumps(data))
# async
#    req=cli.submit_job(workfn, data, wait_until_complete=False)
#    res = cli.wait_until_jobs_completed([req], poll_timeout=5.0)
    print req.state, req.result


