# this is where teh database models goes, import db object from init
from operator import truediv
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique= True)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)

class Post(db.Model):

    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(255))
    post_content = db.Column(db.String(10000))
    enter_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

class Comment(db.Model):

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    enter_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete="CASCADE"), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.String, db.ForeignKey('user.id',ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.String, db.ForeignKey('post.post_id',ondelete="CASCADE"), nullable=False)
