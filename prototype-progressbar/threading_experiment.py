from flask import Flask, render_template
from threading import Thread
from time import sleep
import json

app = Flask(__name__)
status = None

def task():
  global status
  for i in range(1,11):
    status = i
    sleep(1)

@app.route('/')
def index():
  t1 = Thread(target=task)
  t1.start()
  return render_template('index.html')
  
@app.route('/status', methods=['GET'])
def getStatus():
  statusList = {'status':status}
  return json.dumps(statusList)

if __name__ == '__main__':
  app.run(debug=True)