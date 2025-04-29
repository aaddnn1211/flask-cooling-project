from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from project.app import
 app

class EquipmentForm(FlaskForm):
    name = StringField('Ekipman Adı', validators=[DataRequired(), Length(min=2, max=100)])
    quantity = IntegerField('Miktar', validators=[DataRequired(), NumberRange(min=1)], default=1)
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    notes = TextAreaField('Notlar')
    category_id = SelectField('Kategori', coerce=int, validators=[DataRequired()])
    image = FileField('Resim', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Sadece resim dosyaları yüklenebilir!')
    ])
    submit = SubmitField('Kaydet')
