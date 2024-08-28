from flask import Blueprint, render_template, flash, request, jsonify, current_app, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Post
from . import mongo
from bson import ObjectId
import json
import logging
from werkzeug.utils import secure_filename
import os
import traceback
from datetime import datetime

views = Blueprint('views', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'website/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note cannot be empty', category='error')
        else:
            user_id = current_user.get_id()
            new_note = Note.create(data=note, user_id=user_id)
            flash('Note added', category='success')
    
    notes = Note.find_by_user_id(current_user.get_id())
    
    return render_template("home.html", user=current_user, notes=notes)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    try:
        note_id = request.json.get('noteId')
        print("Received delete request for note ID:", note_id)  # Add this line
        if not note_id:
            return jsonify({'success': False, 'error': 'No note ID provided'}), 400

        
        object_id = ObjectId(note_id)

        result = mongo.db.notes.delete_one({'_id': object_id, 'user_id': ObjectId(current_user.get_id())})
        if result.deleted_count == 1:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Note not found or not authorized'}), 404
    except Exception as e:
        print(f"Error in delete_note: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@views.route('/get-notes', methods=['GET'])
@login_required
def get_notes():
    notes = Note.find_by_user_id(current_user.get_id())
    note_list = [{
        '_id': str(note['_id']),
        'data': note['data'],
        'date': note['date'].isoformat()
    } for note in notes]
    print("Sending notes:", note_list)  # Add this line
    return jsonify(note_list)

@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        content = request.form.get('content')
        file = request.files.get('file')
        filename = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        if len(content) < 1:
            flash('Content cannot be empty', category='error')
        else:
            user_id = current_user.get_id()
            new_post = Post.create(content=content, user_id=user_id, image_filename=filename)
            flash('Post created', category='success')
            return redirect(url_for('views.feed'))

    return render_template("create_post.html", user=current_user)

@views.route('/feed', methods=['GET'])
@login_required
def feed():
    posts = Post.find_all()
    return render_template("feed.html", user=current_user, posts=posts)

@views.route('/vietnam', methods=['GET'])
def vietnam():
    return render_template("vietnam.html")

@views.route('/thailand')
def thailand():
    return render_template("thailand.html")

@views.route("/get-journal-entries")
@login_required
def get_journal_entries():
    entries = list(mongo.db.journal_entries.find().sort("timestamp", -1))
    for entry in entries:
        entry["_id"] = str(entry["_id"])
    return jsonify(entries)

@views.route("/create-journal-entry", methods=["POST"])
@login_required
def create_journal_entry():
    content = request.json.get("content")
    entry = {
        "content": content,
        "author": current_user.email,  # Use email instead of username
        "timestamp": datetime.utcnow()
    }
    result = mongo.db.journal_entries.insert_one(entry)
    entry["_id"] = str(result.inserted_id)
    return jsonify(entry)

@views.route("/update-journal-entry", methods=["POST"])
@login_required
def update_journal_entry():
    id = request.json.get("id")
    content = request.json.get("content")
    mongo.db.journal_entries.update_one(
        {"_id": ObjectId(id), "author": current_user.email},  # Use email instead of username
        {"$set": {"content": content}}
    )
    updated_entry = mongo.db.journal_entries.find_one({"_id": ObjectId(id)})
    updated_entry["_id"] = str(updated_entry["_id"])
    return jsonify(updated_entry)

@views.route("/delete-journal-entry", methods=["POST"])
@login_required
def delete_journal_entry():
    id = request.json.get("id")
    result = mongo.db.journal_entries.delete_one({"_id": ObjectId(id), "author": current_user.email})  # Use email instead of username
    return jsonify({"success": result.deleted_count > 0})

@views.route('/create-note', methods=['POST'])
@login_required
def create_note():
    try:
        content = request.json.get('content')
        if not content:
            return jsonify({'success': False, 'error': 'Content cannot be empty'}), 400

        user_id = current_user.get_id()
        new_note = Note.create(data=content, user_id=user_id)
        return jsonify({
            'success': True,
            'note': {
                '_id': str(new_note.id),
                'data': new_note.data,
                'date': new_note.date.isoformat()
            }
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500