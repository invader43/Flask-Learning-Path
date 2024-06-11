## Intro
Basically we will be building a blog style application , something that looks like this .<img src="image.png" alt="drawing" width="350" align='right'/>\
Multiple users can be registered , there will be a login page , a resettable password , account info , profile picture etc. A fullblown blog page.

We wil have to deal with 
- Databases
- Form inputs
- Saving pictures into a backend File system
- Sending Emails for Resetting passwords


&nbsp; 

## Required Packages
- Flask

Follow thru the tutorial using this - [file](https://github.com/invader43/Flask-Learning-Path/blob/main/src/flaskblog/flaskblogPart1.py)
## Running Flask in 2 ways
### Way 1 -Via cli using flask run
For doing this , open your shell , set environment variable :

For mac and linux
```sh
export FLASK_APP = ".\flaskblog.py"
```
For Windows
```bash
set FLASK_APP = ".\flaskblog.py"

or 

 $env:FLASK_APP = ".\flaskblog.py"
```
### Way 2 - Thru Python
Details in comments
```py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Home Page</h1>"



#Easier way to run it would be to run via python
# if the script is run directly , __name__ - a dunder var
# is "__main__" 
if __name__ == "__main__" :
    app.run(debug=True)
```

## Debug Mode 
To enable debug mode while running in cli , we need to set the environment variable 

```sh
FLASK_DEBUG = 1
```
Doing it in windows , mac and linux and mentioned above.\
In part 2 we talk about how to serve templates 

Thats all for today .