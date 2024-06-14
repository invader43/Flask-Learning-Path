from flask import render_template,url_for,flash,redirect
from flaskblog.forms import RegForm , LoginForm
from flaskblog.models import User,Post
from flaskblog import app

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
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!','success')
        return redirect(url_for('home'))
    
    
    return render_template('register.html' , title='Register', form = form)


@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Logged in succesfully' , 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed , please check your login credentials' , 'danger')
    
    return render_template('login.html' , title='Login', form = form)
