from flask import Flask, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)

@app.route('/')
def hello_world():
  return render_template('hello.html')

@app.route('/signUp')
def signUp():
  return render_template('signUp.html')

@app.route('/index')
def home():
    return render_template('index.html')

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