from . import ma
from .models import *
from marshmallow import pre_dump

class TopicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Topic

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ClipSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Clip

class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question

class UserQuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User_Question
