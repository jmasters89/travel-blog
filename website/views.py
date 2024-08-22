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
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note cannot be empty', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
            
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    logger.debug(f"Received delete note request. Data: {request.data}")
    try:
        data = json.loads(request.data)
        logger.debug(f"Parsed data: {data}")
        note_id = data.get('noteID') or data.get('noteId')  # Check for both keys
        logger.debug(f"Note ID to delete: {note_id}")
        if note_id:
            note = Note.query.get(note_id)
            logger.debug(f"Found note: {note}")
            if note and note.user_id == current_user.id:
                db.session.delete(note)
                db.session.commit()
                logger.debug("Note deleted successfully")
                return jsonify({'result': 'success'})
            else:
                logger.warning("Note not found or unauthorized")
                return jsonify({'result': 'fail', 'error': 'Note not found or unauthorized'})
        else:
            logger.warning("NoteID not provided")
            return jsonify({'result': 'fail', 'error': 'NoteID not provided'})
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({'result': 'fail', 'error': str(e)}), 500
