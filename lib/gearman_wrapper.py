import gearman
from config import *

class GearmanWrapper:
    
    def __init__(self):
        self.connections = [config["gearman"]["job_server"]]
        self.prefix = config["gearman"]["job_prefix"]
    
    def client(self, job, data):
        self.gm_client = gearman.GearmanClient(self.connections)
        self.gm_client.submit_job(self.jobName(job), data, background=True, wait_until_complete=False)
    
    def worker(self, registrations):
        self.gm_worker = gearman.GearmanWorker(self.connections)
        for job, fn in registrations.iteritems():
            self.gm_worker.register_task(self.jobName(job), fn)
            
        self.gm_worker.work()
     
    def jobName(self, job):
        return (self.prefix + job).encode('latin-1')