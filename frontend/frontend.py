from flask import Flask, render_template, json, request, redirect, send_file
from bson import json_util
from flask_bootstrap import Bootstrap
import requests
from io import BytesIO, StringIO
from PIL import Image
import base64
import array

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

def checkLogin(template):
  #checks to see if user
  x = requests.get('http://localhost:5000/isLoggedIn')
  res = x.json()
  
  if(res['data'] == "True"):
    print("logged in")
    return redirect("http://localhost:3000/home")
  else:
    return render_template(template)

@app.route('/')
def launch():
  #checks to see if user
  return checkLogin('launch.html')
  

@app.route('/signUp')
def signUp():
  return checkLogin('signUp.html')

@app.route('/login')
def login():
  return checkLogin('login.html')

@app.route('/home')
def home():
  x = requests.get('http://localhost:5000/isLoggedIn')
  res = x.json()
  
  if(res['data'] == "True"):
    x = requests.get('http://localhost:5000/pullFiles')
    res = x.json()
      
    return render_template('home.html', value=res['data'])
    #return send_file(BytesIO(base64.b64decode(imageSource)), attachment_filename=str(res['data'][0][2]), as_attachment=True)#render_template('home.html', value=res['data'])
  else:
    return redirect("http://localhost:3000/")

@app.route('/upload')
def upload():
  x = requests.get('http://localhost:5000/isLoggedIn')
  res = x.json()
  
  if(res['data'] == "True"):
    return render_template('upload.html')
  else:
    return redirect("http://localhost:3000/")
  

@app.route('/downloadFile', methods=['POST'])
def downloadFile():
  document = request.form.to_dict()
  return send_file(BytesIO(base64.b64decode(document['binary'])), attachment_filename=document['filename'], as_attachment=True)

if __name__ == '__main__':
  app.run(host="localhost", port=3000, debug=True)