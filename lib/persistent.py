import redis
import json
import sys
from config import *
from pprint import pprint

class Persistent(object):
    key = None
    _data = None
    redis = None
    deleteFlag = False
    
    def __init__(self, key = None):
        self.key = key
        self.load()
        
    def save(self):
        if(self.deleteFlag):
            self.connection().delete(self.key)
            return self
    
        if self.data() is not None:
            redis_value = json.dumps(self.data())
            self.connection().set(self.key, redis_value)
            return self
        else: 
            raise ValueError("No data was set for persistent data on save")
        
    def load(self):
        redis_value = self.connection().get(self.key)
        
        # get will return None if there is no key, so we don't wanna overwrite with empty
        if redis_value is not None:
            self.set(json.loads(redis_value))
            return self
        else:
            return None
    
    def set(self, data):
        self._data = data;
        return self;
    
    def data(self):
        return self._data
    
    def delete(self):
        self._data = None
        self.deleteFlag = True
    
    def isEmpty(self):
        return self.data() is None
    
    def connection(self):
        if(self.redis is None):
            self.redis = redis.Redis(host = config["redis"]["host"], port = config["redis"]["port"], db = config["redis"]["db"])
        return self.redis
