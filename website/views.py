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