from lib.gearman_wrapper import *
from lib.publisher import *
from pprint import pprint


def publish_listener(gearman_worker, gearman_job):
    print "Received publisher request: " + gearman_job.data
    
    publisher = Publisher()
    return publisher.publish(gearman_job.data)
    
if __name__ == "__main__":
    g = GearmanWrapper()
    g.worker({
        "publish": publish_listener
    })