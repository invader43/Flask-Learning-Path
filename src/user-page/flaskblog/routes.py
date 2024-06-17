from flask import render_template,url_for,flash,redirect,request
from flaskblog.forms import RegForm , LoginForm , UpdateAccountForm
from flaskblog.models import User,Post
from flaskblog import app,bcrypt,db
from flask_login import login_user, current_user , logout_user , login_required
posts = [
    {
        'author': 'dr blake',
        'title': 'Blog 1',
        'content': 'hello world this is my first blog page',
        'date_posted':'August 1,2024'
    },
    {
        'author': 'dr blake',
        'title': 'Blog 2',
        'content': 'This is the second post for testing this template',
        'date_posted':'August 2,2024'
    }
]



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)


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


@app.route("/account" , methods = ['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
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