from flask import render_template,url_for,flash,redirect,request,abort
import secrets # for generating hex 
import os # for getting file type 
from PIL import Image
from flaskblog.forms import (RegForm , LoginForm , UpdateAccountForm , PostForm ,
                              RequestResetForm , ResetPasswordForm)
from flaskblog.models import User,Post
from flaskblog import app,bcrypt,db
from flask_login import login_user, current_user , logout_user , login_required


from datetime import datetime, timedelta

def time_ago_string(past_datetime):
    current_datetime = datetime.utcnow()
    time_difference = current_datetime - past_datetime

    # Calculate time difference in seconds
    seconds_diff = time_difference.total_seconds()
    # Determine the appropriate time ago string based on the time difference
    if seconds_diff < 60:
        return f"{int(seconds_diff)} seconds ago"
    elif seconds_diff < 3600:
        minutes_diff = seconds_diff / 60
        return f"{int(minutes_diff)} minutes ago"
    elif seconds_diff < 86400:
        hours_diff = seconds_diff / 3600
        return f"{int(hours_diff)} hours ago"
    elif seconds_diff < 604800:
        days_diff = seconds_diff / 86400
        return f"{int(days_diff)} days ago"
    elif seconds_diff < 31536000:
        weeks_diff = seconds_diff / 604800
        return f"{int(weeks_diff)} weeks ago"
    else:
        years_diff = seconds_diff / 31536000
        return f"{int(years_diff)} years ago"



@app.route("/") 
@app.route("/home")
def home():
    page = request.args.get('page' , 1 , type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page = page)
    print(posts)
    return render_template('home.html', posts = posts , datetimefunc = time_ago_string)


@app.route("/about")
def aboutme():
    return render_template('about.html',title='about')


@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegForm()
    if current_user.is_authenticated:
        flash(f"You're already logged in",'success')
        return redirect(url_for('home'))

    if form.validate_on_submit():
        #first generate hashedPassword
        hashedPass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        #now add the user into the database
        userNew = User(username = form.username.data , email = form.email.data , password = hashedPass)

        # add and commit to database 
        db.session.add(userNew)
        db.session.commit()

        flash(f'Account Created for {form.username.data}! , you will now be able to login using your account credentials','success')
        return redirect(url_for('login'))
    
    
    return render_template('register.html' , title='Register', form = form)


@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash(f'Youre already logged in','success')
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

    # We check if user exist by passing on user , and perform a hash check from database
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user( user , remember = form.remember.data)
            next_page = request.args.get('next')
            if next_page :
                return redirect(next_page)
            return redirect(url_for('home'))
        else :
            flash('Login Failed , please check your login credentials' , 'danger')
    
    return render_template('login.html' , title='Login', form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    # its not good to store the filename thats sent thru user 
    # its not even good to use username to store filename , if image files leak 
    # using the secrets module to generate a hex 
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path , 'static/profile_pics' , picture_filename)

    output_size = (125,125)

    image_resized = Image.open(form_picture)
    image_resized.thumbnail(output_size)
    image_resized.save(picture_path)

    return picture_filename

@app.route("/account" , methods = ['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        #checking if picture file is uploaded
        if form.picture.data :
            old_picture_path = os.path.join(app.root_path , 'static/profile_pics' , current_user.image_file)
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
        return redirect(url_for('account'))
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


@app.route("/post/new" , methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data , content = form.content.data , author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created' , 'success')
        return redirect(url_for('home'))
    

    
    return render_template('create_post.html',title='New Post' , 
                           form = form , legend = 'New Post' )


@app.route("/post/<int:post_id>")
def post(post_id):
    # We need to use get or 404 in cases we dont know if the query fails or passes
    # before hand 
    post = Post.query.get_or_404(post_id)

    return render_template('post.html' , title = post.title , post = post , datetimefunc = time_ago_string )


@app.route("/post/<int:post_id>/update" , methods = ['GET' , 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        print(post.author , current_user )
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Updated" , 'success')
        return redirect(url_for('post' , post_id = post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html',title='Update Post' , 
                           form = form , legend ='Update Post')

#Removed get request , we want to accept only post requests for this route from that modal
@app.route("/post/<int:post_id>/delete" , methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post Updated" , 'success')
    return redirect(url_for('home'))



@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page' , 1 , type = int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page = page)
    print(posts)
    return render_template('user_posts.html', posts = posts , datetimefunc = time_ago_string , user = user )


