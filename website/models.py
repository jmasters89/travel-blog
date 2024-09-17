from replit import db
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
import os
import uuid

class Note:
    def __init__(self, data, user_id, author):
        self.data = data
        self.date = datetime.now(timezone.utc)
        self.user_id = user_id
        self.author = author
        self.id = str(uuid.uuid4())

    @classmethod
    def create(cls, data, user_id, author):
        note = cls(data, user_id, author)
        note_key = f"note:{note.id}"
        db[note_key] = {
            'data': note.data,
            'date': note.date.isoformat(),
            'user_id': note.user_id,
            'author': note.author
        }
        return note

    @classmethod
    def find_by_user_id(cls, user_id):
        notes = []
        for key in db.keys():
            if key.startswith('note:'):
                note_data = db[key]
                if note_data['user_id'] == user_id:
                    notes.append(note_data)
        return notes

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
        new_user_key = f"user:{email}"
        db[new_user_key] = {
            'email': email,
            'password': password,
            'first_name': first_name
        }
        return cls(email, email, password, first_name)

    @classmethod
    def find_by_email(cls, email):
        user_key = f"user:{email}"
        user_data = db.get(user_key)
        if user_data:
            return cls(
                email,  # Using email as ID
                user_data['email'],
                user_data['password'],
                user_data['first_name']
            )
        return None

    @classmethod
    def find_by_id(cls, user_id):
        user_key = f"user:{user_id}"
        user_data = db.get(user_key)
        if user_data:
            return cls(
                user_id,
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
        self.id = str(uuid.uuid4())

    @classmethod
    def create(cls, content, user_id, image_filename=None):
        post = cls(content, user_id, image_filename)
        post_key = f"post:{post.id}"
        db[post_key] = {
            'content': post.content,
            'date': post.date.isoformat(),
            'user_id': post.user_id,
            'image_filename': post.image_filename
        }
        return post

    @classmethod
    def find_all(cls):
        posts = []
        for key in db.keys():
            if key.startswith('post:'):
                post_data = db[key]
                posts.append(post_data)
        # Sort posts by date in descending order
        posts.sort(key=lambda x: x['date'], reverse=True)
        return posts

class JournalEntry:
    def __init__(self, content, author, country, timestamp=None, photo_filename=None):
        self.content = content
        self.author = author
        self.country = country
        self.timestamp = timestamp or datetime.utcnow()
        self.photo_filename = photo_filename
        self.id = str(uuid.uuid4())

    @classmethod
    def create(cls, content, author, country, photo=None):
        photo_filename = None
        if photo:
            filename = secure_filename(photo.filename)
            photo_filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
            photo.save(os.path.join('website', 'static', 'uploads', photo_filename))

        entry = cls(content, author, country, photo_filename=photo_filename)
        entry_key = f"journal_entry:{entry.id}"
        db[entry_key] = {
            'content': entry.content,
            'author': entry.author,
            'country': entry.country,
            'timestamp': entry.timestamp.isoformat(),
            'photo_filename': entry.photo_filename
        }
        return entry

    @classmethod
    def find_by_country(cls, country):
        entries = []
        for key in db.keys():
            if key.startswith('journal_entry:'):
                entry_data = db[key]
                if entry_data['country'] == country:
                    entries.append(entry_data)
        entries.sort(key=lambda x: x['timestamp'], reverse=True)
        return entries