from flask.ext.wtf import Form
from wtforms import SubmitField, TextField, TextAreaField
from wtforms.validators import Required


class CreateThreadForm(Form):
    name = TextField(validators=[Required()])
    content = TextAreaField(validators=[Required()])
    submit = SubmitField()


class CreatePostForm(Form):
    content = TextAreaField(validators=[Required()])
    submit = SubmitField()


class EditPostForm(CreatePostForm):
    pass
