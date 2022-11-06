from flask import Blueprint, request, jsonify
from flask import Flask, jsonify

import validators
from src.constants.http_status_code import *
auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
from src.database import User,db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity




@auth.post('/register')
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if len(password) < 6:
        return jsonify(
            {
                'error' : 'Password is too short'
            }
        ),HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify(
            {
                'error' : 'User Name is too short'
            }
        ),HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST


    if not validators.email(email):
        return jsonify(
            {
                'error': 'Email is not valid '
            }
        ), HTTP_400_BAD_REQUEST

    if User.select().where(User.email==email).first() is not None:
        return jsonify(
            {
                'error': 'Email is already taken '
            }
        ), HTTP_409_CONFLICT

    if User.select().where(User.username==username).first() is not None:
        return jsonify(
            {
                'error': 'Username is already taken '
            }
        ), HTTP_409_CONFLICT

    pwd_password = generate_password_hash(password)

    with db.transaction() as txn:
        User.create(username=username, password=pwd_password, email=email)
        txn.commit()

    return jsonify(
        {
            'message': 'User Created',
            'user':
                {
                    'username': username,
                    'email': email
                }

        }
    ), HTTP_201_CREATED



@auth.post('/login')
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.select().filter(User.email==email).first()
    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email
                }

            }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED



@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK