from persistent import *

class State(Persistent):
    
    # encode state names bytestring
    def data(self):
        state_name = super(State, self).data()
        if state_name is not None:
            return state_name.encode('latin-1')
        else:
            return state_name