from flask import Flask, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/signUp')
def signUp():
  return render_template('signUp.html')

@app.route('/signIn')
def signIn():
  return render_template('signIn.html')

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/upload')
def upload():
  return render_template('upload.html')

@app.route('/view')
def view():
  return render_template('view.html')

@app.route('/profile')
def profile():
  return render_template('profile.html')

if __name__ == '__main__':
  app.run(host="localhost", port=3000, debug=True)