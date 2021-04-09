"""
Flask endpoints to make

1. Add New User
 -> input
    uniqname
-> What it does
 -> output
    {user_id: ''}
    success
2. Return List of questions they have to do (18)
output: [
        {question_id: int, topic:"", option_1: {embed_link:"", transcript:""}, option_2:{...},...},
        {...},
        ..
        ]
3. Submit answers to a given question
input: {
            question_id:
            user_id:
            best_option:
            worst_option:
        }
"""

from flask import request, abort, Response, Blueprint, jsonify
import json
from app import app
from app.models import db
from app.models.models import Clip, Question
from app.models.schema import ClipSchema, QuestionSchema
import requests

# @app.route('/api/update_questions/', methods=['PUT'])
# def UpdateQuestions():
#     topic_file = 'Infrared_Radiation_v1_id.txt.tuples'
#     topic_id = 84
#     with open(topic_file, 'r') as f:
#         for line in f:
#             data = line.split()
#             #get data
#             option_1_id=data[0]
#             option_2_id=data[1]
#             option_3_id=data[2]
#             option_4_id=data[3]
#
#             #clean data
#
#             #add data
#             new_question = Question(option_1_id=option_1_id, option_2_id=option_2_id, option_3_id=option_3_id, option_4_id=option_4_id, topic_id=topic_id)
#             db.session.add(new_question)
#             print(option_1_id, '|', option_2_id, '|', option_3_id, '|', option_4_id, '|', topic_id)
#         db.session.commit()
#     return Response(status=200)

# @app.route('/api/update_clips/', methods=['PUT'])
# def UpdateClips():
#     topic_file = 'Infrared_Radiation_v1.txt'
#     topic_id = 84
#     with open(topic_file, 'r') as f:
#         for line in f:
#             try:
#                 data = line.split('|')
#                 #get data
#                 start_time=data[1]
#                 video_key = data[3]
#                 transcript = data[4]
#                 clip_id = data[5]
#
#                 #clean data
#                 start_time = float(start_time)
#                 start_time = int(start_time)
#                 clip_id = int(clip_id)
#
#                 #add data
#                 new_clip = Clip(clip_id=clip_id, embed_link=('https://www.youtube.com/embed/'+video_key), start_time=start_time, transcript=transcript, topic_id=topic_id)
#                 db.session.add(new_clip)
#                 print(clip_id, '|', video_key, '|', start_time, '|', topic_id)
#
#             except:
#                 print("error:", line)
#
#         db.session.commit()
#     return Response(status=200)
