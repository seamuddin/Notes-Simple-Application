from flask import Blueprint, request, jsonify
from  werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, jsonify
import validators
from src.constants.http_status_code import *
note = Blueprint("note", __name__, url_prefix="/api/v1/note")
from src.database import db, Notes
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity


@note.route('/', methods=['POST', 'GET'])
@jwt_required()
def create_note():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        tags = request.form.get('tags')

        current_user = get_jwt_identity()


        with db.transaction() as note:

            Notes.create(title=title, body=body, tag=tags,user_id=current_user)
            note.commit()


        return jsonify({
            'message': 'Note Created',
            'note':
                {
                    'title': title,
                    'body': body,
                    'tags': tags
                }
        }), HTTP_201_CREATED




# @note.route('/',methods=['POST','GET'])
# def note():
#     if request.method=='POST':
        # current_user = get_jwt_identity()

        # title = request.form.get('title')
        # body = request.form.get('body')
        # tags = request.form.get('tags')

        # note = Notes(title=title, body=body,tags=tags, user_id=current_user)
        # note.commit


        # with db.transaction() as note:
        #
        #     Notes.create(title=title, body=body, tags=tags)
        #     note.commit()

    # return jsonify(
    #     {
    #         'message': 'Note Created',
    #         'user':
    #             {
    #                 'title': title,
    #                 'body': body,
    #                 'tags':tags
    #             }
    #
    #     }
    # ), HTTP_201_CREATED



