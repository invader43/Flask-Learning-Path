## Forms and User Input using WTForms 
For this section we are going to use WTForms , as a flask extension , called flask-wtforms , this basically simplifies a form into a class designed using the inbuilt elements given in the module.

To install it using pip , 

```sh
pip install flask-wtf
```

In the wtf package , we have form elements and their validators that we can import and directly inherit a base class called FlaskForm for creating our forms. We can redirect this form directly using the app.route decorator in the main application.

```python
#Base class for forms
from flask_wtf import FlaskForm

#Field Classes for creating fields with different elements
from wtforms import StringField , PasswordField , SubmitField , BooleanField

#Validators for returning erros on wrong input
from wtforms.validators import DataRequired, Length , Email , EqualTo
```

We can design forms using the OOP pattern , below is an example you can follow:

```python
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
```

Now if you wonder how to use this class RegForm , we have to create an instance of the RegForm inside our main application to use it .
```python
from flask import Flask,render_template,url_for,flash,redirect
app = Flask(__name__)

@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!','success')
        return redirect(url_for('home'))
    
    
    return render_template('register.html' , title='Register', form = form)
```

Now all the backend is set , we have to use jinja to create the register.html from the layout.html . 
One example div is showcased below

```jinja
<div class="form-group">
    {{ form.username.label(class="form-control-label") }}

    {% if form.username.errors %}
        {{ form.username(class="form-control form-control-lg is-invalid")}}
        <div class="invalid-feedback">
            {% for error in form.username.errors %}
            <span> {{ error }} </span>
            {% endfor %}
        </div>
        {% else %}
            {{ form.username(class="form-control form-control-lg")}}
    {% endif %}

</div>
```
See the else block ,
```jinja
{{ form.username(class="form-control form-control-lg")}}
```
This is now a form element is created , the class tag is for bootstrap classes , for making it look more good ( I have to learn CSS and bootstrap to understand this 😔😔)

Now how do we display the errors that are printed from validation , remember we used Validators for each form element , for that is the if statement , 
```jinja
{% if form.username.errors %}
    {{ form.username(class="form-control form-control-lg is-invalid")}}
    <div class="invalid-feedback">
        {% for error in form.username.errors %}
        <span> {{ error }} </span>
        {% endfor %}
    </div>
```
This gives out all the errors as a span , meaning new line for each error below the form element ( form.username) , these messages are stored inside the wtforms.validators class , we dont need to reinvent the wheel , we need to learn how to use it for now.

Thats all for this tutorial. For more info on the bootstrap classes used , follow this link ➡️ [Link](https://getbootstrap.com/docs/5.0/forms/form-control/).