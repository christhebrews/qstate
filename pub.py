'''
    State Queue (qstate) Publication Endpoint
    This file serves as a utility for publishing queue state to the adapters (see configuration file)
    It connects from the primary web endpoint over gearman.  This file busy-waits until gearman provides a gearman

    @see lib/publisher.py for publication logic

    @see http://gearman.org/ for gearman overview
    @see https://pythonhosted.org/gearman/ for python implementation
    @see lib/gearman_wrapper.py for technical implementation
'''

from lib.gearman_wrapper import *
from lib.publisher import *
from pprint import pprint

'''
publish_listener()
This is an implementation on the gearman worker,
@param gearman_worker 
@param gearman_job object
'''
def publish_listener(gearman_worker, gearman_job):
    print "Received publisher request: " + gearman_job.data
    
    publisher = Publisher()
    return publisher.publish(gearman_job.data)
    
if __name__ == "__main__":
    g = GearmanWrapper()
    g.worker({
        "publish": publish_listener
    })