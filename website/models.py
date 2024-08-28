from . import mongo
from flask_login import UserMixin
from bson.objectid import ObjectId
from datetime import datetime, timezone

class Note:
    def __init__(self, data, user_id):
        self.data = data
        self.date = datetime.now(timezone.utc)
        self.user_id = user_id

    @classmethod
    def create(cls, data, user_id):
        note = cls(data, user_id)
        result = mongo.db.notes.insert_one({
            'data': note.data,
            'date': note.date,
            'user_id': ObjectId(user_id)
        })
        note.id = result.inserted_id
        return note

    @classmethod
    def find_by_user_id(cls, user_id):
        return list(mongo.db.notes.find({'user_id': ObjectId(user_id)}))

class User(UserMixin):
    def __init__(self, id, email, password, first_name):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name

    def get_id(self):
        return str(self.id)

    @classmethod
    def create(cls, email, password, first_name):
        result = mongo.db.users.insert_one({
            'email': email,
            'password': password,
            'first_name': first_name
        })
        return cls(str(result.inserted_id), email, password, first_name)

    @classmethod
    def find_by_email(cls, email):
        user_data = mongo.db.users.find_one({'email': email})
        if user_data:
            return cls(
                str(user_data['_id']),
                user_data['email'],
                user_data['password'],
                user_data['first_name']
            )
        return None

    @classmethod
    def find_by_id(cls, user_id):
        try:
            object_id = ObjectId(user_id)
        except:
            return None
        user_data = mongo.db.users.find_one({'_id': object_id})
        if user_data:
            return cls(
                str(user_data['_id']),
                user_data['email'],
                user_data['password'],
                user_data['first_name']
            )
        return None

class Post:
    def __init__(self, content, user_id, image_filename=None):
        self.content = content
        self.date = datetime.utcnow()
        self.user_id = user_id
        self.image_filename = image_filename

    @classmethod
    def create(cls, content, user_id, image_filename=None):
        post = cls(content, user_id, image_filename)
        result = mongo.db.posts.insert_one({
            'content': post.content,
            'date': post.date,
            'user_id': ObjectId(user_id),
            'image_filename': post.image_filename
        })
        post.id = result.inserted_id
        return post

    @classmethod
    def find_all(cls):
        return list(mongo.db.posts.find().sort('date', -1))