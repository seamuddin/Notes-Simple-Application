from flask import Blueprint, request, jsonify
from  werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, jsonify
import validators
from src.constants.http_status_code import *
note = Blueprint("note", __name__, url_prefix="/api/v1/note")
from src.database import db, Notes
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from peewee import *

@note.route('/', methods=['POST', 'GET'])
@jwt_required()
def create_note():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        tags = request.form.get('tags')

        with db.atomic() as transaction:
            try:
                Notes.create(title=title, body=body, tag=tags, user_id=current_user)
                transaction.commit()
                return jsonify({
                    'message': 'Note Created',
                    'note':
                        {
                            'title': title,
                            'body': body,
                            'tags': tags
                        }
                }), HTTP_201_CREATED
            except DatabaseError:
                transaction.rollback()
                return jsonify({'error': 'Notes Can not Create'}), HTTP_406_NOT_ACCEPTABLE





    else:
        notes = Notes.select().where(Notes.user_id==current_user)

        data = []
        for i in notes:
            data.append(
                {
                    'title': i.title,
                    'body': i.body,
                    'tag':i.tag

                }
            )

        return jsonify({
            'data':data
        }),HTTP_200_OK

    return jsonify({'error': 'Notes Can not Create'}), HTTP_406_NOT_ACCEPTABLE


@note.put('/<int:id>')
@jwt_required()
def update_notes(id):
    current_user = get_jwt_identity()
    if request.method == 'PUT':
        title = request.form.get('title')
        body = request.form.get('body')
        tags = request.form.get('tags')

        if title and body and tags:

            with db.atomic() as transaction:
                try:
                    note = Notes.get(id=id)
                    note.title = title
                    note.body = body
                    note.tag =  tags
                    note.user_id = current_user
                    note.save()
                    return jsonify({
                        'message': 'Note Updated',
                        'note':
                            {
                                'title': note.title,
                                'body': note.body,
                                'tags': note.tag
                            }
                    }), HTTP_200_OK
                except DatabaseError:
                    transaction.rollback()
                    return jsonify({'error': 'Notes Can not Update'}), HTTP_406_NOT_ACCEPTABLE

    return jsonify({'error': 'Notes Can not Update'}), HTTP_406_NOT_ACCEPTABLE




@note.delete('/<int:id>')
@jwt_required()
def delete_note(id):
    current_user = get_jwt_identity()
    if request.method == 'DELETE':
        if id:
            with db.atomic() as transaction:
                try:
                    Notes.delete().where(Notes.id==id)
                    transaction.commit()
                    return jsonify({
                        'message': 'Note Deleted'
                    }), HTTP_200_OK
                except DatabaseError:
                    transaction.rollback()
                    return jsonify({'error': 'Notes Can not Update'}), HTTP_406_NOT_ACCEPTABLE
        return jsonify({'error': 'Notes Can not Delete'}), HTTP_406_NOT_ACCEPTABLE
