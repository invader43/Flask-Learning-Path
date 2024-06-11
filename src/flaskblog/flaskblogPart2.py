from flask import Flask,render_template,url_for
app = Flask(__name__)

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



#Easier way to run it would be to run via python
# if the script is run directly , __name__ - a dunder var
# is "__main__" 
if __name__ == "__main__" :
    app.run(debug=True)
