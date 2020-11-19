from flask import Flask, render_template, json, request, redirect
from bson import json_util
import sqlite3 as sql
from PIL import Image
import face_recognition
import io
import base64

username = ""
isLoggedIn = False

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
def hello_world():
  return Response(200, "hello, world!").serialize()

@app.route('/isLoggedIn')
def isIn():
  global isLoggedIn
  return Response(200, str(isLoggedIn)).serialize()

@app.route('/logout')
def logout():
  global isLoggedIn
  isLoggedIn = False
  return redirect("http://localhost:3000/")

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
  global isLoggedIn
  global username
  #make sure user email isnt already in use
  #make sure username isnt is already in use 
  #IF WE HAVE TIME MAKE SURE THERES A FACE IN THE PICTURE
  if request.method == 'POST':
    document = request.form.to_dict()

    with sql.connect("vault.db") as con:
      cur = con.cursor()
      cur.execute('SELECT * FROM User WHERE EXISTS (SELECT * FROM User WHERE Username = "' + document['username'] + '" OR Email = "' + document['email'] + '"' + ')' )
    result = cur.fetchall()

    
    if(len(result) == 0):
      image = request.files['image']
      blob = image.read()
    
      with sql.connect("vault.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO User (Username, Email, FaceRef, Security1, Security2, Security3) VALUES (?,?,?,?,?,?)", (document['username'], document['email'], blob, document['sec1'], document['sec2'], document['sec3']))
      
      isLoggedIn = True
      username = document['username']

      return redirect("http://localhost:3000/home")
      #return Response(200, ["image uploaded successfully to the database!", document['username'], document['email'], document['sec1'], document['sec2'], document['sec3']]).serialize()
    else: 
      return Response(200, "A user with that email or username already exists!").serialize()


@app.route('/login', methods=['GET', 'POST'])
def signIn():
  global isLoggedIn
  global username
  error = False

  if request.method == 'POST':
    document = request.form.to_dict()
    #at this point we need to do TWO THINGS
    #1. ensure we are passing over the image from the frontend and not just the file name (Orlando)
    #2. pull from the db and check the images against each other using the format of the example in newFace.py
    
    with sql.connect("vault.db") as con:
      cur = con.cursor()
      cur.execute('SELECT FaceRef, Security1, Security2, Security3 FROM User WHERE Username = "' + document['username'] + '"')
    result = cur.fetchall()
    
    #print(result)
    if len(result) > 0: 
      #0 is the blob, 1 is security question one, 2 is security question two, 3 is security question three
      #4 is security question 3
      imageSource = result[0][0]
      sec1 = result[0][1]
      sec2 = result[0][2]
      sec3 = result[0][3]
      
      if (document['sec1'] != sec1) or (document['sec2'] != sec2) or (document['sec3'] != sec3):
        error = True
      
      if error is False:
        #look into image compressing 
        image = request.files['image']
        blob = image.read()
        
        img = Image.open(image.stream)
        img.save("submitted.jpg")
        
        with open('database.jpg', 'wb') as f:
          f.write(imageSource)
        
        loginImage = face_recognition.load_image_file("submitted.jpg")
        unknown_encoding = face_recognition.face_encodings(loginImage)[0]

        dbImage = face_recognition.load_image_file("database.jpg")
        known_encoding = face_recognition.face_encodings(dbImage)[0]

        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        results = results[0]

        if results == True:
          msg = "Weclome, " + document['username'] + "!"
          isLoggedIn = True
          username = document['username']
          return redirect("http://localhost:3000/home")
        else:
          msg = "Access Denied: You are not " + document['username'] + "."
          return Response(200, msg).serialize()
        
      else:  
        return Response(200, "You answered a security question wrong.").serialize()
    
    else:
      error = True
    return Response(200, "User not found in database").serialize()
    
  else:
    return Response(200, "not allowed").serialize()

@app.route('/uploadFiles', methods=['GET', 'POST'])
def upload_files():
  global isLoggedIn
  global username
  if request.method == 'POST': 
    #inserts new files into database
    if isLoggedIn == True:
      for uploaded_file in request.files.getlist('files'):
        if uploaded_file.filename != '':
            print("file here")
            nameOfFile = uploaded_file.filename
            blob = uploaded_file.read()
            print(blob)
            with sql.connect("vault.db") as con:
              cur = con.cursor()
              cur.execute("INSERT INTO Files (Owner, FileName, File) VALUES (?,?, ?)", (username, nameOfFile, blob))
      return redirect("http://localhost:3000/home")
    else:
      return redirect("http://localhost:3000/")
  
@app.route('/pullFiles', methods=['GET', 'POST'])
def pull_files():
  global isLoggedIn
  global username
  #if request.method == 'POST': 
  res = []
  #inserts new files into database
  if isLoggedIn == True:
    with sql.connect("vault.db") as con:
      cur = con.cursor()
      cur.execute("SELECT * FROM Files WHERE Owner= ?", (username,))
      res = cur.fetchall()

      #for row in res:
        #print(row[2])
            
      return Response(200, res).serialize()
  else:
    return redirect("http://localhost:3000/")

  

if __name__ == '__main__':
  app.run(host="localhost", port=5000, debug=True)
  