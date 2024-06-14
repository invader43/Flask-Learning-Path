from flask import Flask,render_template,url_for,flash,redirect
from forms import RegForm , LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




app = Flask(__name__)
app.config['SECRET_KEY'] = '03c846950425a22fc22fb6be5f12ef6d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# models 

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20) , unique=True, nullable = False)
    email = db.Column(db.String(120) , unique=True, nullable = False)
    image_file = db.Column(db.String(20) , nullable = False , default = 'default.jpg')
    password = db.Column(db.String(60) , nullable = False)
    posts = db.relationship('Post' , backref ='author' , lazy = True)
    # Post because we are referencing the Class


    #how our object is printed 
    def __repr__(self):
        return f"User('{self.username}','{self.email}' , '{self.image_file}' )"
    



class Post(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100) , nullable = False)
    date_posted = db.Column(db.DateTime , nullable = False , default = datetime.utcnow )
    content = db.Column(db.Text , nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    # The table 
    #how  our object is printed 
    def __repr__(self):
        return f"User('{self.title}' , '{self.date_posted}' )"


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




if __name__ == "__main__" :
    app.run(debug=True)
