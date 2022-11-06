from flask import Flask, jsonify
import os
from src.database import db
from src.auth import auth
from src.note import note
from src.constants.http_status_code import *
from flask_jwt_extended import JWTManager
def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    if __name__ == '__main__':
        app.run(debug=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY =os.environ.get("dev"),
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
        )
    else:
        app.config.from_mapping(test_config)


    app.register_blueprint(auth)
    app.register_blueprint(note)

    JWTManager(app)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app