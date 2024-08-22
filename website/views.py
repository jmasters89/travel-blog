from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import logging

views = Blueprint('views', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note cannot be empty', category='error')
        else:
            new_note = Note(data=note)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    
    notes = Note.query.all()
    
    if current_user.is_authenticated:
        return render_template("home.html", user=current_user, notes=notes)
    else:
        return render_template("home.html", user=None, notes=notes)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    try:
        data = json.loads(request.data)
        note_id = data.get('noteID') or data.get('noteId')  # Check for both keys
        note = Note.query.get(note_id)
        if note:
            db.session.delete(note)
            db.session.commit()
            return jsonify({'result': 'success'})
        else:
            return jsonify({'result': 'fail', 'error': 'Note not found'})
    except Exception as e:
        logger.error(f"Error in delete_note: {str(e)}")
        return jsonify({'result': 'fail', 'error': str(e)}), 500
