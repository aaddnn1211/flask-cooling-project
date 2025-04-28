from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    content = TextAreaField('Yorum', validators=[DataRequired()])
    submit = SubmitField('Gönder')
