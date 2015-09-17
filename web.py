from flask import Flask, request, jsonify, render_template
from lib.publisher import *
app = Flask(__name__)

@app.route("/push", methods=["POST"])
def push():
    state = getPostData(request)["state"]
    
    if state is None or not state:
        return jsonify(success = False, error = "Invalid state string")
    else:
        publisher = Publisher()
        return jsonify(success = publisher.addState(state))

@app.route("/next", methods=["POST"])
def next():
    publisher = Publisher()
    publisher.increment()
    return jsonify(active_state = publisher.getActive())

@app.route("/state", methods=["GET"])
def state():
    publisher = Publisher()
    return jsonify(active_state = publisher.getActive())

@app.route("/debug", methods=["GET"])
def debug():
    publisher = Publisher()
    return jsonify(
        queue = publisher.getQueue(),
        active_state = publisher.getActive()
    )

def getPostData(request):
    if request.get_json() is not None:
        return request.get_json()
    elif request.form is not None:
        return request.form
    else:
        return {}
            
    
# TEMPORARY
from lib.persistent import *
    
@app.route("/testSetState", methods=["POST"])
def testApi():
    print "hit test api"
    state = getPostData(request)["state"]
    s = Persistent('test').set(state)
    s.save()
    return "complete"
    
@app.route("/test")
def test():
    return render_template('test.html')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

