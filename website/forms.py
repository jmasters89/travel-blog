from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired

class JournalEntryForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    location = SelectField('Location', choices=[('Vietnam', 'Vietnam'), ('Thailand', 'Thailand')], validators=[DataRequired()])
    image = FileField('Image')