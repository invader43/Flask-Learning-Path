from flask import Blueprint
from flask import render_template,url_for,flash,redirect,request,current_app
import os # for getting file type 
from flaskblog.users.forms import (RegForm , LoginForm , UpdateAccountForm ,
                              RequestResetForm , ResetPasswordForm)
from flaskblog.models import User,Post
from flaskblog import bcrypt,db
from flask_login import login_user, current_user , logout_user , login_required
from flaskblog.users.utils import time_ago_string , send_reset_email ,save_picture

users = Blueprint('users', __name__ )

# adding routes that have everything to do with user

@users.route("/register", methods = ['GET','POST'])
def register():
    form = RegForm()
    if current_user.is_authenticated:
        flash(f"You're already logged in",'success')
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        #first generate hashedPassword
        hashedPass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        #now add the user into the database
        userNew = User(username = form.username.data , email = form.email.data , password = hashedPass)

        # add and commit to database 
        db.session.add(userNew)
        db.session.commit()

        flash(f'Account Created for {form.username.data}! , you will now be able to login using your account credentials','success')
        return redirect(url_for('users.login'))
    
    
    return render_template('register.html' , title='Register', form = form)


@users.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash(f'Youre already logged in','success')
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

    # We check if user exist by passing on user , and perform a hash check from database
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user( user , remember = form.remember.data)
            next_page = request.args.get('next')
            if next_page :
                return redirect(next_page)
            return redirect(url_for('main.home'))
        else :
            flash('Login Failed , please check your login credentials' , 'danger')
    
    return render_template('login.html' , title='Login', form = form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account" , methods = ['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        #checking if picture file is uploaded
        if form.picture.data :
            old_picture_path = os.path.join(current_app.root_path , 'static/profile_pics' , current_user.image_file)
            if os.path.isfile(old_picture_path): os.remove(old_picture_path)
            # a new function called save_picture() , note that save_picture also creates a new file
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        #  add the user into the database
        current_user.username = form.username.data
        current_user.email = form.email.data
        # flask_login automates the process of adding it into the database ,
        # we dont need to do the db.session.add here , we can do this manually , 
        # but it would make the code redundant 
        db.session.commit()
        flash("Your Account has been updated" , 'success')
        return redirect(url_for('users.account'))
        # why not render template instead of redirect  - ?? Post Get Redirect Pattern 
        # "are you sure you want to reload this page " , redirect sends a get request
        # read more here en.wikipedia.org/wiki/Post/Redirect/Get
    

    # Basically if we are visiting the site after a login , and user is seeing it after
    # a get request , we want to populate the form with the current username and email
    elif request.method == 'GET' :
        form.username.data = current_user.username
        form.email.data = current_user.email


    #setting the image file , now we send it to our template
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # https://peps.python.org/pep-0008/ talking about pep8 compliance
    return render_template('account.html' ,title = 'Account' ,image_file = image_file , form=form) 

@users.route("/reset_password" , methods = ['GET' , 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Reset Password email sent to your email")
        return redirect(url_for('users.login'))


    return render_template('reset_request.html' , title ='Reset Password' , form = form )


@users.route("/reset_password/<token>" , methods = ['GET' , 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_token(token)

    if user is None :
        flash('That token is invalid/expired , get a new token for resetting password' , 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #first generate hashedPassword
        hashedPass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # add and commit to database 
        user.password = hashedPass
        db.session.commit()

        flash(f'Account password updated','success')
        return redirect(url_for('users.login'))


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page' , 1 , type = int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page = page)
    print(posts)
    return render_template('user_posts.html', posts = posts , datetimefunc = time_ago_string , user = user )


