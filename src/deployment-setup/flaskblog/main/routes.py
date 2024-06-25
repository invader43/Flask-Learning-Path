from flask import render_template,request,Blueprint
from flaskblog.models import Post
from flaskblog.users.utils import time_ago_string
main = Blueprint('main', __name__ )


@main.route("/") 
@main.route("/home")
def home():
    page = request.args.get('page' , 1 , type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page = page)
    print(posts)
    return render_template('home.html', posts = posts , datetimefunc = time_ago_string)


@main.route("/about")
def aboutme():
    return render_template('about.html',title='about')


