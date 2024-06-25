from flask import ( Blueprint , render_template , url_for, flash , redirect ,
                   request , abort )
from flaskblog.users.utils import time_ago_string
from flaskblog import db
from flask_login import current_user
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flask_login import login_required
posts = Blueprint('posts', __name__ )

#crud routes for posts
@posts.route("/post/new" , methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data , content = form.content.data , author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created' , 'success')
        return redirect(url_for('main.home'))
    

    
    return render_template('create_post.html',title='New Post' , 
                           form = form , legend = 'New Post' )


@posts.route("/post/<int:post_id>")
def post(post_id):
    # We need to use get or 404 in cases we dont know if the query fails or passes
    # before hand 
    post = Post.query.get_or_404(post_id)

    return render_template('post.html' , title = post.title , post = post , datetimefunc = time_ago_string )


@posts.route("/post/<int:post_id>/update" , methods = ['GET' , 'POST'])
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
        return redirect(url_for('posts.post' , post_id = post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html',title='Update Post' , 
                           form = form , legend ='Update Post')

#Removed get request , we want to accept only post requests for this route from that modal
@posts.route("/post/<int:post_id>/delete" , methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post Updated" , 'success')
    return redirect(url_for('main.home'))
