from src import create_app
from flask import Flask, jsonify, render_template
from . import database
app = Flask(__name__)
application = create_app()



@app.get("/")
def say_hello():
    return render_template('home.html')
