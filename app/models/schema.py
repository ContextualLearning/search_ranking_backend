from . import ma
from .models import *
from marshmallow import pre_dump

class ClassSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Class

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class FileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = File

class VideoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Video
        exclude = ['transcript']

class UserClassSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User_Class
