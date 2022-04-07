import flask
from flask import request
from ruler import Ruler
import threading

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/', methods=['GET'])
def home():
    return "<div style='display: flex; align-items:center; justify-content: center; width: 100%; height: 100%;'><h1 style='font-size: 48px; color: #12f5ee'>Ruling app</h1></div>"

@app.route('/api/ruler', methods=['POST'])
def ruler():
    email = request.json['email']
    password = request.json['password']

    ruler = Ruler()
    try:
        ruler.startRuling(email, password)
        return "success"
    except:
        return "failed"

app.run(host="0.0.0.0", port=int("80"))