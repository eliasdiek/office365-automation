import flask
from flask import request, jsonify
from ruler import Ruler
import threading

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<div style='display: flex; align-items:center; justify-content: center; width: 100%; height: 100%;'><h1 style='font-size: 48px; color: #12f5ee'>Ruling app</h1></div>"

@app.route('/api/ruler/normal', methods=['POST'])
def normalRuler():
    email = request.json['email']
    password = request.json['password']

    ruler = Ruler()
    try:
        ruler.normalRuling(email, password)
        return "success"
    except:
        return "failed"

@app.route('/api/ruler/godaddy', methods=['POST'])
def godaddyRuler():
    email = request.json['email']
    password = request.json['password']

    ruler = Ruler()
    try:
        ruler.godaddyRuling(email, password)
        return "success"
    except:
        return "failed"

app.run()