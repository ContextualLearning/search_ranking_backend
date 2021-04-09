from . import db
import datetime
import json
import enum

class semesterEnum(str, enum.Enum):
    FA = 'FA'
    WN = 'WN'
    SP = 'SP'
    SU = 'SU'

class Class(db.Model):
    __tablename__ = 'class'

    class_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    email= db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    title= db.Column(db.String(128), nullable=False, unique=True)
    semester=db.Column(db.Enum(semesterEnum))
    year=db.Column(db.Integer)
    active=db.Column(db.Boolean)
    cache_name=db.Column(db.String(128))
    join_code = db.Column(db.String(7))
    search_enabled = db.Column(db.Boolean, nullable=False)
    vid_list_enabled = db.Column(db.Boolean, nullable=False)

    users=db.relationship('User', secondary='user_class', back_populates="classes")

class User(db.Model):
    __tablename__ = 'users'

    user_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    email= db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    firstname=db.Column(db.String(128))
    lastname=db.Column(db.String(128))
    kaltura_key=db.Column(db.Text)

    classes=db.relationship('Class', secondary='user_class', back_populates="users")


class File(db.Model):
    __tablename__ = 'files'

    file_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String(128), nullable=False, unique=True)
    file_link=db.Column(db.Text)
    text=db.Column(db.Text)
    date=db.Column(db.DateTime)
    type=db.Column(db.String(128))
    class_id=db.Column(db.ForeignKey('class.class_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    Class = db.relationship('Class')

class Video(db.Model):
    __tablename__ = 'videos'

    video_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String(128), nullable=False, unique=True)
    video_link=db.Column(db.Text)
    transcript=db.Column(db.String(4294000000))
    date=db.Column(db.DateTime)
    type=db.Column(db.String(128))
    slide=db.Column(db.Text)
    image=db.Column(db.Text)
    class_id=db.Column(db.ForeignKey('class.class_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    Class = db.relationship('Class')

# user_class = db.Table(
#     'user_class',
#     db.Column('user_id', db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
#     db.Column('class_id', db.ForeignKey('class.class_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
# )

class User_Class(db.Model):
    __tablename__ = 'user_class'
    # user_id = db.Column('user_id', db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    # class_id = db.Column('class_id', db.ForeignKey('class.class_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    class_id = db.Column(db.ForeignKey('class.class_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
