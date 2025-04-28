from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ProjectForm(FlaskForm):
    name = StringField('Proje Adı', validators=[DataRequired(), Length(min=3, max=100)])
    location = StringField('Konum', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    notes = TextAreaField('Notlar')
    submit = SubmitField('Kaydet')
