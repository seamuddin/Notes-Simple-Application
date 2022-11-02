from flask import Flask, jsonify

app = Flask(__name__)



@app.get("/")
def say_hello():
    return jsonify({"message":"Hello world"})