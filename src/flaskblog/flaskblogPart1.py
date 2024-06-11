from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "<h1>Home Page</h1>"

@app.route("/about")
def aboutme():
    return "<h1>About Page</h1>"



#Easier way to run it would be to run via python
# if the script is run directly , __name__ - a dunder var
# is "__main__" 
if __name__ == "__main__" :
    app.run(debug=True)
