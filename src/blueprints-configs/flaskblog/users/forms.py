from flask_wtf import FlaskForm 
from flask_wtf.file import FileField , FileAllowed # for having insertable images for profile pic
from wtforms import StringField , PasswordField , SubmitField , BooleanField
from wtforms.validators import DataRequired, Length , Email , EqualTo , ValidationError
from flaskblog.models import User
from flask_login import current_user


class RegForm(FlaskForm):
    username = StringField('Username',validators=[
        DataRequired(),
        Length(min = 5 , max = 20)])
    email = StringField('Email',validators=[
        DataRequired() ,
        Email()
    ])
    password = PasswordField('Password',validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Confirm Password',validators=[
        DataRequired(),
        EqualTo('password')
    ])


    submit = SubmitField('Sign Up')

    # https://wtforms.readthedocs.io/en/2.3.x/forms/#in-line-validators 
    def validate_username(self , username):
        user = User.query.filter_by(username = username.data).first() 
        if user :
            raise ValidationError('Username already exists , Please choose a different one')
        
    def validate_email(self , email):
        user = User.query.filter_by(email = email.data).first() 
        if user :
            raise ValidationError('Email already exists , Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[
        DataRequired() ,
        Email()
    ])
    password = PasswordField('Password',validators=[
        DataRequired()
    ])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Update Account Form 
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[
        DataRequired(),
        Length(min = 5 , max = 20)])
    email = StringField('Email',validators=[
        DataRequired() ,
        Email()
    ])

    picture = FileField('Update Profile Picture' , validators=[FileAllowed(['jpg' , 'png'])])
    submit = SubmitField('Update Details')

    # https://wtforms.readthedocs.io/en/2.3.x/forms/#in-line-validators 
    def validate_username(self , username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first() 
            if user :
                raise ValidationError('Username already exists , Please choose a different one')
        
    def validate_email(self , email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first() 
            if user :
                raise ValidationError('Email already exists , Please choose a different one')
            



class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired() ,Email()])
    
    submit = SubmitField('Request Reset Password')

    def validate_email(self , email):
        user = User.query.filter_by(email = email.data).first() 
        if user is None :
            raise ValidationError("Email doesn't exist , Create an account before resetting the password")
        


            
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Confirm Password',validators=[
        DataRequired(),
        EqualTo('password')
    ])

    submit = SubmitField('Reset Password')  