from flask import Flask, request, abort, Response, Blueprint, jsonify
from flask_cors import CORS, cross_origin
from app.models import db
from . import models
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config.from_object('config')
models.init_app(app)

from app.main import *
