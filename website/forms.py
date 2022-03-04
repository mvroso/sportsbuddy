from datetime import date as date_func
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, Optional
from flask_login import current_user
from website.models import User, Sport

class RegistrationForm(FlaskForm):
	name = StringField('Name',
				validators=[DataRequired(), Length(min=2, max=20)])
	email = EmailField('E-mail Adress',
				validators=[DataRequired(), Email()])
	gender = SelectField('Gender',
				validators=[DataRequired()],
				choices=[(1, "Male"), (2, "Female"),
						(3, "Not applicable")])
	password = PasswordField('Password',
				validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
				validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This e-mail is already been used')


class LoginForm(FlaskForm):
	email = StringField('Email',
				validators=[DataRequired(), Email()])
	password = PasswordField('Password',
				validators=[DataRequired()])
	submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
	email = StringField('email',
				validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('This e-mail is not linked to any account')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password',
				validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
				validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')

class UpdateAccountForm(FlaskForm):
	name = StringField('Name',
				validators=[DataRequired(), Length(min=2, max=20)])
	email = EmailField('E-mail Adress',
				validators=[DataRequired(), Email()])
	picture = FileField('Profile Picture',
					validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('This e-mail is already been used')


# Implementing MatchForm Mixin
class MatchFormMixin():

	title = StringField('Title',
					validators=[DataRequired(), Length(min=2, max=50)])
	description = TextAreaField('Description')

	# DateTime is deprecated
	date = DateField('Match Date', format='%Y-%m-%d',
					validators=[DataRequired()])

	time_period = SelectField('Time Period',
				validators=[DataRequired()],
				choices=[(1, "Morning"), (2, "Afternoon"),
						(3, "Evening"), (4, "Night")])

	location = StringField('Location', validators=[Length(min=2, max=50)])

	sport_id = SelectField('Sport', validators=[DataRequired()])

	# Date validation
	def validate_date(self, date):
		if date.data < date_func.today():
			raise ValidationError("The date cannot be in the past!")

# Create new match Form
class CreateMatchForm(FlaskForm, MatchFormMixin):

    submit = SubmitField('Create Match')

# Update match Form
class UpdateMatchForm(FlaskForm, MatchFormMixin):

    submit = SubmitField('Update Match')


# Filter match Form
class FilterMatchForm(FlaskForm):


	title = StringField('Title',
					validators=[Optional()])
	description = TextAreaField('Description')

	# DateTime is deprecated
	date = DateField('Match Date', format='%Y-%m-%d',
					validators=[Optional()])

	time_period = SelectField('Time Period',
				validators=[Optional()],
				choices=[(1, "Morning"), (2, "Afternoon"),
						(3, "Evening"), (4, "Night")])

	location = StringField('Location', validators=[Optional()])

	sport_id = SelectField('Sport', validators=[Optional()])

	submit = SubmitField('Filter Match')
