# app.py
from random import randint
from flask import request
from flask import Flask
from flask.json import jsonify

app = Flask(__name__)

state = {}
state.update({'sessions': {}})
# defining a route
@app.route("/", methods=['GET', 'POST', 'PUT']) # decorator
def home(): # route handler function
    # returning a response
    return "Hello World!"

@app.route("/getSession/", methods=['GET'])
def getSession():
    sessionID = request.args.get('sid')
    sessions = state['sessions']
    if(sessionID in sessions.keys()):
        return jsonify()
    else:
        sessionID.p

@app.route("/createsession", methods=['POST'])
def createSession():

    code = randint(1000, 9999)
    sessions.
    sessions.update({})
    return "Success: " + sessions.id
app.run(debug = True)
stateDict = dict()