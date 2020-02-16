from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email

class WorkerF(FlaskForm):
    fname = StringField('Enter worker first name', validators=[DataRequired()])
    lname = StringField('Enter worker last name', validators=[DataRequired()])
    address1 = StringField('Enter worker address1', validators=[DataRequired()])
    city = StringField('Enter worker\'s city', validators=[DataRequired()])
    state = StringField('Enter worker\'s state', validators=[DataRequired()])
    country = StringField('Enter worker\'s country', validators=[DataRequired()])
    telephone = StringField('Enter worker\'s telephone number', validators=[DataRequired()])
    role = StringField('Enter worker\'s role', validators=[DataRequired()])
    email = StringField('Enter worker\'s email address', validators=[DataRequired(), Email()])