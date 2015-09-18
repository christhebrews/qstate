'''
    State Queue (qstate) API
    This file serves a public API to recieve requests to manipulate the State Queue
    It utilizes the flask library to serve publically.

    The endpoints exposed are:

    POST /push
        @param state string
        @return {success: bool}
        Pushes a new state to the end of the queue

    POST /next
        @return {active_state: string}
        Iterates on the queue, setting the next state to active_state

    GET /state
        @return {active_state: string}
        Gets the currently active state on the queue

    GET /debug
        @return {active_state: string, queue: array}
        Returns a debug object with the active state and the queue

'''

from flask import Flask, request, jsonify, render_template
from lib.publisher import *
app = Flask(__name__)

# API Endpoint: POST /push
@app.route("/push", methods=["POST"])
def push():
    state = getPostData(request)["state"]
    
    if state is None or not state:
        return jsonify(success = False, error = "Invalid state string")
    else:
        publisher = Publisher()
        return jsonify(success = publisher.addState(state))

# API Endpoint: POST /next
@app.route("/next", methods=["POST"])
def next():
    publisher = Publisher()
    publisher.increment()
    return jsonify(active_state = publisher.getActive())

# API Endpoint: GET /state
@app.route("/state", methods=["GET"])
def state():
    publisher = Publisher()
    return jsonify(active_state = publisher.getActive())

# API Endpoint: GET /debug
@app.route("/debug", methods=["GET"])
def debug():
    publisher = Publisher()
    return jsonify(
        queue = publisher.getQueue(),
        active_state = publisher.getActive()
    )

# Currently "/" is a temporary test application for the API, it renders a template with javascript
# endpoints for testing all of the above API endpoints
# TODO move to unit test
@app.route("/")
def test():
    return render_template('test.html')

'''
    getPostData()
    Utility function for converting post data into the correct format based on passed type (form/rest)
'''
def getPostData(request):
    if request.get_json() is not None:
        return request.get_json()
    elif request.form is not None:
        return request.form
    else:
        return {}

'''
    Web application entrypoint/loader
'''
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

