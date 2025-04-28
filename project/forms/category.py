from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CategoryForm(FlaskForm):
    name = StringField('Kategori Adı', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Açıklama')
    submit = SubmitField('Kaydet')
