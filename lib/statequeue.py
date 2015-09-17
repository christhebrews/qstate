from persistent import *

class StateQueue(Persistent):

    _data = []

    def pop(self):
        if len(self._queue()) > 0:
            return self._queue().pop(0)
        else:
            return False
        
    def push(self, state):
        self._queue().append(state.data())
        return self
    
    def _queue(self):
        return self._data