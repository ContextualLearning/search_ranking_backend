from . import db
import datetime
import json
import enum



class Topic(db.Model):
    __tablename__ = 'topics'

    topic_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String(128))

class User(db.Model):
    __tablename__ = 'users'

    user_id= db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    uniqname= db.Column(db.String(128), nullable=False, unique=True)


class Clip(db.Model):
    __tablename__ = 'video_clips'

    clip_id= db.Column(db.Integer, primary_key=True)
    embed_link=db.Column(db.Text)
    start_time=db.Column(db.Integer, nullable=False)
    transcript=db.Column(db.Text)
    topic_id=db.Column(db.ForeignKey('topics.topic_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    topic = db.relationship('Topic')

class Question(db.Model):
    __tablename__ = 'questions'

    question_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    option_1_id=db.Column(db.ForeignKey('video_clips.clip_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    option_2_id=db.Column(db.ForeignKey('video_clips.clip_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    option_3_id=db.Column(db.ForeignKey('video_clips.clip_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    option_4_id=db.Column(db.ForeignKey('video_clips.clip_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    topic_id=db.Column(db.ForeignKey('topics.topic_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    option_1 = db.relationship('Clip', foreign_keys=[option_1_id])
    option_2 = db.relationship('Clip', foreign_keys=[option_2_id])
    option_3 = db.relationship('Clip', foreign_keys=[option_3_id])
    option_4 = db.relationship('Clip', foreign_keys=[option_4_id])
    topic = db.relationship('Topic', foreign_keys=[topic_id])

# user_class = db.Table(
#     'user_class',
#     db.Column('user_id', db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
#     db.Column('class_id', db.ForeignKey('class.class_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
# )

class User_Question(db.Model):
    __tablename__ = 'user_question'
    # user_id = db.Column('user_id', db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    # class_id = db.Column('class_id', db.ForeignKey('class.class_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    question_id = db.Column(db.ForeignKey('questions.question_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    best_option = db.Column(db.Integer)
    worst_option = db.Column(db.Integer)
