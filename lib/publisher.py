import requests
from statequeue import *
from state import *
from config import *
from gearman_wrapper import *
import redis
import json

class Publisher:
    def __init__(self):
        self.queue = StateQueue('state_queue')
        self.active_state = State('active_state')
    
    def triggerPublish(self):
        gearman = GearmanWrapper()
        gearman.client("publish", self.getActive())
    
    # trigger by gearman
    def publish(self, state = None):
        if state is None:
            state = self.getActive()
    
        post = {"state": state}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        for api in config["adapters"]:
            print "Running api request: " + api["code"]
            r = requests.post(api["url"], data=json.dumps(post), headers=headers)
            if r.status_code > 200:
                print "Error recieved running request against " + api["url"]
                print r.text
        
        return state # gearman needs a string return? weird
    
    def increment(self):
        state = self.queue.pop()
        if state:
            self.active_state.set(state)
        else:
            self.active_state.delete()
        
        self.queue.save()
        self.active_state.save()
        
        if self.getActive():
            self.triggerPublish(); # trigger with gearman
        
        return self.getActive()
    
    def getQueue(self):
        return self.queue.data()
    
    def getActive(self):
        return self.active_state.data()
    
    def addState(self, state_data):
        s = State().set(state_data)
        self.queue.push(s).save()
        return True