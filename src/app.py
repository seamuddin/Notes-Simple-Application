from flask import Flask, jsonify
from . import database
app = Flask(__name__)



@app.get("/")
def say_hello():
    return jsonify({"message":"Hello world"})


@app.get("/test")
def test():

    database.User.create()

