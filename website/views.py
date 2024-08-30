from flask import Blueprint, render_template, flash, request, jsonify, current_app, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Post, User, JournalEntry  # Add JournalEntry here
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

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    try:
        note_id = request.json.get('noteId')
        print("Received delete request for note ID:", note_id)  # Add this line
        if not note_id:
            return jsonify({'success': False, 'error': 'No note ID provided'}), 400

        
        notes = db.get('notes', [])
        notes = [note for note in notes if note['id'] != note_id or note['user_id'] != current_user.get_id()]
        db['notes'] = notes

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error in delete_note: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@views.route('/get-notes', methods=['GET'])
def get_notes():
    notes = list(db.get('notes', []))
    note_list = []
    for note in notes:
        author = 'Anonymous'
        if 'user_id' in note:
            user = User.find_by_id(str(note['user_id']))
            if user:
                author = user.first_name
        note_list.append({
            '_id': str(note['_id']),
            'data': note['data'],
            'date': note['date'].isoformat(),
            'author': author
        })
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
    return render_template("vietnam.html", user=current_user, country="vietnam")

@views.route('/thailand')
def thailand():
    return render_template("thailand.html", user=current_user, country="thailand")

@views.route("/get-journal-entries/<country>")
def get_journal_entries(country):
    try:
        entries = JournalEntry.find_by_country(country)
        result = []
        for entry in entries:
            author_user = User.find_by_id(entry["author"])
            author_email = author_user.email if author_user else "Unknown"
            entry_dict = {
                "_id": str(entry["_id"]),
                "content": entry["content"],
                "author_id": entry["author"],
                "author_email": author_email,
                "country": entry["country"],
                "timestamp": entry["timestamp"].isoformat(),
                "is_author": current_user.is_authenticated and str(entry["author"]) == str(current_user.id),
                "photo": f"/static/uploads/{entry['photo_filename']}" if entry.get('photo_filename') else None
            }
            result.append(entry_dict)
        print(f"Entries: {result}")  # Add this line for debugging
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_journal_entries: {str(e)}")
        return jsonify({"error": f"An error occurred while fetching journal entries: {str(e)}"}), 500

@views.route("/create-journal-entry", methods=["POST"])
@login_required
def create_journal_entry():
    content = request.form.get('content')
    country = request.form.get('country')
    photo = request.files.get('photo')

    if not content:
        return jsonify({"error": "Content is required"}), 400

    try:
        entry = JournalEntry.create(content, str(current_user.id), country, photo)
        return jsonify({
            "_id": str(entry.id),
            "content": entry.content,
            "author_id": entry.author,
            "author_email": current_user.email,
            "country": entry.country,
            "timestamp": entry.timestamp.isoformat(),
            "photo": f"/static/uploads/{entry.photo_filename}" if entry.photo_filename else None,
            "is_author": True
        }), 201
    except Exception as e:
        current_app.logger.error(f"Error creating journal entry: {str(e)}")
        return jsonify({"error": "An error occurred while creating the journal entry"}), 500

@views.route("/update-journal-entry", methods=["POST"])
@login_required
def update_journal_entry():
    try:
        id = request.json.get("id")
        content = request.json.get("content")
        
        if not id or not content:
            return jsonify({"error": "Missing id or content"}), 400

        result = db.get('journal_entries', [])
        result = [entry for entry in result if entry['id'] != id or entry['author'] != current_user.get_id()]
        db['journal_entries'] = result

        return jsonify({"success": True, "message": "Entry updated successfully"}), 200

    except Exception as e:
        current_app.logger.error(f"Error updating journal entry: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@views.route("/delete-journal-entry", methods=["POST"])
@login_required
def delete_journal_entry():
    try:
        id = request.json.get("id")
        
        if not id:
            return jsonify({"success": False, "message": "Missing entry id"}), 400

        result = db.get('journal_entries', [])
        result = [entry for entry in result if entry['id'] != id or entry['author'] != current_user.get_id()]
        db['journal_entries'] = result

        return jsonify({"success": True, "message": "Entry deleted successfully"}), 200

    except Exception as e:
        current_app.logger.error(f"Error deleting journal entry: {str(e)}")
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500

@views.route('/create-note', methods=['POST'])
@login_required
def create_note():
    try:
        content = request.json.get('content')
        if not content:
            return jsonify({'success': False, 'error': 'Content cannot be empty'}), 400

        user_id = current_user.get_id()
        new_note = Note.create(data=content, user_id=user_id, author=current_user.first_name)
        return jsonify({
            'success': True,
            'note': {
                '_id': str(new_note.id),
                'data': new_note.data,
                'date': new_note.date.isoformat(),
                'author': current_user.first_name
            }
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500