from flask import Flask, render_template, json, request
from bson import json_util
from flask_bootstrap import Bootstrap
app = Flask(__name__)

class Response:
    def __init__(self, code, data, *args):
        # An HTTP Response code
        # See a list here: https://www.restapitutorial.com/httpstatuscodes.html
        self.code = code

        # Use getResponseData to get status and message params.
        self.status = getResponseData(code)['status']
        self.message = getResponseData(code)['message']

        # Pass thru data from constructor.
        #print("data = ", data)
        self.data = data

        # Pass thru optional errorData dict, to help describe an error.
        self.errorData = args[0] if len(args)>0 else {}

    def serialize(self):
        return json_util.dumps(self.__dict__), {'Content-Type': 'application/json; charset=utf-8'}

def getResponseData(code):
    # Dict containing all possible response codes
    possibleCodes = {
        200: {"status": "Success", "message": "The request completed successfully"},
        401: {"status": "Login Error", "message": "We could not authenticate your login credentials"},
        404: {"status": "Failure", "message": "The resource requested could not be found"}
    }

    # errObj, the default response when a code is not found in the possibleCodes dict
    errObj = {"status": "Fatal Error", "message": "The code returned does not correspond with a status! Contact an admin for help."}

    # Return the code's corresponding dict
    return possibleCodes.get(code, errObj)

@app.route('/')
def launch():
  return render_template('launch.html')

@app.route('/signUp')
def signUp():
  return render_template('signUp.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/upload')
def upload():
  return render_template('upload.html')


if __name__ == '__main__':
  app.run(host="localhost", port=3000, debug=True)