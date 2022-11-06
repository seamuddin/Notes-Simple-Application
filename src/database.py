from peewee import *
from datetime import datetime

db = SqliteDatabase('main.db')

class User(Model):
    id = IntegerField(primary_key=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(null = False)
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    class Meta:
        database = db

    def __repr__(self):
        return self.username

class Notes(Model):
    id = IntegerField(primary_key=True)
    title = CharField()
    body = CharField()
    user = ForeignKeyField(User, backref='notes')
    tag = CharField()

    class Meta:
        database = db

    def __repr__(self):
        return self.title

