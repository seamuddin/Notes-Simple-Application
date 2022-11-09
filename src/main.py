from flask import Flask, jsonify, render_template, Blueprint
from . import database
home = Blueprint("home", __name__, url_prefix="/")

@home.get("/")
def say_hello():
    return render_template('home.html')
