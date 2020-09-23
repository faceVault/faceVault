from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Frontend'

if __name__ == '__main__':
  app.run(host="localhost", port=5000, debug=True)