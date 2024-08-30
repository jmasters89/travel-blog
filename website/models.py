from replit import db
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
import os
import json

class Note:
    @classmethod
    def create(cls, data, user_id, author):
        note = {
            'data': data,
            'date': str(datetime.now(timezone.utc)),
            'user_id': user_id,
            'author': author
        }
        if 'notes' not in db:
            db['notes'] = []
        notes = db['notes']
        notes.append(note)
        db['notes'] = notes
        return note

    @classmethod
    def find_by_user_id(cls, user_id):
        return [note for note in db.get('notes', []) if note['user_id'] == user_id]

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
        if 'users' not in db:
            db['users'] = []
        users = db['users']
        new_user = {
            'id': str(len(users)),
            'email': email,
            'password': password,
            'first_name': first_name
        }
        users.append(new_user)
        db['users'] = users
        return cls(**new_user)

    @classmethod
    def find_by_email(cls, email):
        users = db.get('users', [])
        user_data = next((user for user in users if user['email'] == email), None)
        return cls(**user_data) if user_data else None

    @classmethod
    def find_by_id(cls, user_id):
        users = db.get('users', [])
        user_data = next((user for user in users if user['id'] == user_id), None)
        return cls(**user_data) if user_data else None

class Post:
    @classmethod
    def create(cls, content, user_id, image_filename=None):
        post = {
            'content': content,
            'date': str(datetime.utcnow()),
            'user_id': user_id,
            'image_filename': image_filename
        }
        if 'posts' not in db:
            db['posts'] = []
        posts = db['posts']
        posts.append(post)
        db['posts'] = posts
        return post

    @classmethod
    def find_all(cls):
        return sorted(db.get('posts', []), key=lambda x: x['date'], reverse=True)

class JournalEntry:
    @classmethod
    def create(cls, content, author, country, photo=None):
        photo_filename = None
        if photo:
            filename = secure_filename(photo.filename)
            photo_filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
            photo.save(os.path.join('website', 'static', 'uploads', photo_filename))

        entry = {
            'content': content,
            'author': author,
            'country': country,
            'timestamp': str(datetime.utcnow()),
            'photo_filename': photo_filename
        }
        if 'journal_entries' not in db:
            db['journal_entries'] = []
        entries = db['journal_entries']
        entries.append(entry)
        db['journal_entries'] = entries
        return entry

    @classmethod
    def find_by_country(cls, country):
        try:
            entries = [entry for entry in db.get('journal_entries', []) if entry['country'] == country]
            entries.sort(key=lambda x: x['timestamp'], reverse=True)
            print(f"Found {len(entries)} entries for country: {country}")
            return entries
        except Exception as e:
            print(f"Error in find_by_country: {str(e)}")
            raise