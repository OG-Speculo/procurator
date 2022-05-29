from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField,IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
import phonenumbers


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class RegisterForm(FlaskForm):
    email_address = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    name = StringField(label='Name', validators=[DataRequired()])
    radio_btn = RadioField(label="radio button", choices=[("Manager", "Manager"), ("Employee", "Employee")], default="Manager", validate_choice=[DataRequired()])
    submit = SubmitField(label='Register')


class DonorDetailsForm(FlaskForm):
    work = StringField(label='Work Done', validators=[Length(max=50), DataRequired()])
    hours = IntegerField(label="No. of Hours", validators=[DataRequired()])
    submit = SubmitField(label='submit')
