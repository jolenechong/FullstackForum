from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, logout_user, current_user
from .models import User, Post,  Comment, Like
from . import db
import json

# setting up blueprint
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    post = Post.query.with_entities(Post).distinct()
    if request.method == 'POST':
        post_title = request.form.get('post_title')
        post_content = request.form.get('post_content')

        if len(post_title) < 1 and len(post_content)< 1:
            flash("You can't submit an empty post", category='error')
        else:
            # adding note
            new_note = Post(post_title=post_title,post_content=post_content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Post added!', category='success')

    return render_template("home.html", user=current_user, post = post)

@views.route('/delete-note', methods=["POST"])
def delete_note():
    # request data is a string of the noteid
    note = json.loads(request.data)
    # access noteId attribute
    noteId = note['noteId']
    note = Post.query.get(noteId)

    if note:
        # if user whos signed in owns this note, return response
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route("/edit-post/<id>")
@login_required
def edit_note(id):
    post = Post.query.filter_by(post_id=id).first()

# getting from url parameters
    post_title = request.args.get('post_title')
    post_content = request.args.get('post_content')

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.user_id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        # post.update({Post.post_title : post_title, Post.post_content : post_content})
        post.post_title = post_title
        post.post_content = post_content
        db.session.commit()
        flash('Post Updated!.', category='success')

    post = Post.query.with_entities(Post).distinct()
    return redirect(url_for('views.home'))

    
# @views.route('/like-post/<post_id>', methods=["GET"])
# @login_required
# def like(post_id):
#     post = Post.query.filter_by(id=post_id)
#     like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

#     if not post:
#         flash("Post does not exist", category='error')
#     elif like:
#         db.session.delete(like)
#         db.session.commit()
#     else:
#         like = Like(user_id=current_user.id, post_id=post_id)
#         db.session.add(like)
#         db.session.commit()
#     return render_template("home.html", user=current_user, post = post)

@views.route('/create-comment/<post_id>', methods=['POST'])
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty', category='error')
    else:
        post = Post.query.filter_by(post_id=post_id)
        if post:
            comment = Comment(user_id=current_user.id, post_id=post_id, text = text)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist', category='error')

    return redirect(url_for('views.home'))

@views.route('/delete-comment/<comment_id>')
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist', category='error')
    elif current_user.id != comment.user_id and current_user.id !=comment.post.user_id:
        flash('You do not have the permission to delete this comment', category='errpr')
    else:
        db.session.delete(comment)
        db.session.commit() 
        
    return redirect(url_for('views.home'))

@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    like = Like.query.filter_by(
        user_id=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.user_id, post.likes)})