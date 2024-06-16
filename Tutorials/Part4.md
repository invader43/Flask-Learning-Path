## Databases with SQLAlchemy
SQL Alchemy is a very popular Object Relational Mapper ( ORM for short ) , which basically allows us to access a database via OOP methods instead of relying on SQL Queries. Also having an ORM allows us to use different database for Production and Debugging , for example SQLite database is usually used for debugging , and for Production a Postgres database is used. Since SQLite is lightweight its used for debugging.

Further reading about ORMs ➡️ [Link](https://stackoverflow.com/questions/448684/why-should-you-use-an-orm)

We start by installing the flask sqlalchemy package , is an extension for flask.

```sh
pip install flask-sqlalchemy
```


We can initialize a SQLAlchemy Database by setting the Flaskapp variables as follows 
```python 
app.config['SECRET_KEY'] = '03c846950425a22fc22fb6be5f12ef6d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
```
SECRET_KEY is used have sessions inside a web app , for more info see this [Stack Overflow Answer](https://stackoverflow.com/a/48596852).


This talks about SQLALCHEMY_DATABASE_URI variable , and how to set it if you want a local sqlite3 database or a postgres database server login credentials. ➡️ [Link](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)

SQLAlchemy takes in the Flask app variable as argument , setting up the database for the app automatically.
```python 
db = SQLAlchemy(app)
```
This is how Flask extensions work in general , take in the app and return the object relevant to the Extension.

### Database Tables 
In the object oriented patterns , analogous to tables we have Models , we use the base class db.Model to create our Models( essentially tables). One example is given below:

```python 
class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(20) , unique=True, nullable = False)
    email = db.Column(db.String(120) , unique=True, nullable = False)
    image_file = db.Column(db.String(20) , nullable = False , default = 'default.jpg')
    password = db.Column(db.String(60) , nullable = False)
    posts = db.relationship('Post' , backref ='author' , lazy = True)
    # Post because we are referencing the Class
    # code for Post is given in src folder 


    #how our object is printed 
    def __repr__(self):
        return f"User('{self.username}','{self.email}' , '{self.image_file}' )"
```

This above User class is basically the SQL CREATE statement given below :
```SQL
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    image_file VARCHAR(20) NOT NULL DEFAULT 'default.jpg',
    password VARCHAR(60) NOT NULL
);
```

The dunder method \_\_repr\_\_() is used for showing the general representation upon query inside the python shell , queries return a list with default arguments , where the \_\_repr\_\_() comes into picture.

Lets go inside the python shell to understand this...

```python
>>> from flaskblog import db #flaskblog is the current file name

>>> db.create_all() #creates a file called site.db in the instance folder
#Lets create a new user to learn how to do it 
>>> from flaskblog import User,Post
>>> user1 = User(username = 'invader43' , email = 'invader@gmail.com' , password='passwd' )
# This creates a user1 variable , this does nothing to db we dont reference it anywhere yet 
# To add it into the database we have to call the db.session.add()
>>> db.session.add(user1)
#Note that even this doesnt change anything in the site.db
#To make changes to the database we have to call the db.session.commit()
>>> db.session.commit()
```
We can perform queries for a table/model using Model.query.all()

```python
>>> User.query.all()
[User('invader43' , 'invader@gmail.com' , 'default.jpg' ) , User('John' , 'john@gmail.com' , 'default.jpg' )]
#now you understand what the __repr__() method does

>>> User.query.first()
[User('invader43' , 'invader@gmail.com' , 'default.jpg' )]
```

There are other methods , like query.filter_by , get() etc. You can read all this in detail here ➡️ [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/)

Relationships are possible , using a foreign key for a post , retrieving the foreign key for a post and querying it in the User Model , gives the user details for a post , all these are SQL concepts ported onto OOP patterns. I prefer that you see the code for yourself and understand this part - [Link to code](https://github.com/invader43/Flask-Learning-Path/blob/main/src/databases/flaskblog.py)