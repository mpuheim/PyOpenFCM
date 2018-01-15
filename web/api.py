from ..lib.fcm import FCM
import json
from flask import Flask
app = Flask(__name__)

@app.route("/")
def info():
    s="""
    Welcome to FCM service:<br/>
    <br/>
    Help:<br/>
    1. Create new FCM at <a href="/fcm">/fcm</a><br/>
    2. Get your online FCM at <a href="/get/ID">/get/ID</a><br/>
    3. Load your FCM at <a href="/load">/load</a><br/>
    """
    return s

@app.route("/get/<ID>")
def get(ID):
    map = FCM()
    map.add("C1")
    map.add("C2")
    map.connect("C1","C2")
    s=json.dumps(map.__dict__)#TODO
    return s

# entry point for the application
if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)
