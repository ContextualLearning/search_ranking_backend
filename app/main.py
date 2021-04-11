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

from flask import request, abort, Response, Blueprint, jsonify, render_template, session, redirect, url_for
from  sqlalchemy.sql.expression import func
import json
from app import app
from app.models import db
from app.models.models import User,Clip, Question, Topic, User_Question
from app.models.schema import ClipSchema, QuestionSchema
import requests

MAX_QUESTIONS = 17
# SESSION_TYPE = 'filesystem'

def get_questions():
    topics = Topic.query.all()

    # get 2 from each topic
    questions = []
    for topic in topics:
        two_questions = Question.query.filter_by(topic_id=topic.topic_id).order_by(func.random()).limit(2)
        #two_questions_json = QuestionSchema(many=True).jsonify(two_questions).json
        for question in two_questions:
            option_1 = ClipSchema().jsonify(question.option_1).json
            option_2 = ClipSchema().jsonify(question.option_2).json
            option_3 = ClipSchema().jsonify(question.option_3).json
            option_4 = ClipSchema().jsonify(question.option_4).json
            questions.append({'topic':topic.title, 'question_id':question.question_id, 'option_1':option_1, 'option_2':option_2, 'option_3':option_3, 'option_4':option_4})
        #questions.extend(two_questions_json)

    return questions

@app.route('/', methods=['GET'])
def home():
    if 'user_id' in session:
        return redirect(url_for('show_question', id = '1'))

    return render_template('login.html')

@app.route('/new_user/', methods=['POST', 'GET'])
def new_user():

    uniqname = request.form.get('uniqname')
    print(uniqname)
    if not uniqname:
        abort(404)

    print('ok')
    user = User.query.filter_by(uniqname=uniqname).first()
    print(user)
    if user:
        session['user_id'] = user.user_id
        return redirect(url_for('show_question', id='1'))

    new_user = User(uniqname=uniqname)
    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)

    # 1. generate the questions
    # 2. for each questions, add to use_question table without best and worst option
    user_id = jsonify({'user_id':new_user.user_id})
    print(user_id)

    question = get_questions()
    # print(question)
    # print(json.dumps(question))

    print(new_user.user_id)

    for i in question:
    # for i in range(5):
      user_id = new_user.user_id
      question_id = i['question_id']
      print(str(user_id) + ' '+ str(question_id))
    #   print(question_id)
      best_option = None
      worst_option = None
      new_answer = User_Question(user_id=user_id, question_id=question_id, best_option=best_option, worst_option=worst_option)
      db.session.add(new_answer)
      db.session.commit()

    session['user_id'] = new_user.user_id

    return redirect(url_for('show_question',id='1'))

@app.route('/show_question/<id>', methods=['POST', 'GET'])
def show_question(id):

    print('okkkk')
    print(session)
    if 'user_id' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        print('notokkk')
        id = request.form.get('id')
        print(id)
        return redirect(url_for('show_question', id = str(id)))
    
    user_questions = User_Question.query.filter_by(user_id=session['user_id']).order_by(User_Question.question_id.asc())

    session['curr_q_id'] = int(id)

    # if 'curr_q_id' not in session:
    #     session['curr_q_id'] = id
    # else:
    #     session['curr_q_id'] = (session['curr_q_id'] + 1) % MAX_QUESTIONS


    # set context based on index
    q_id = user_questions[session['curr_q_id']].question_id

    question = Question.query.filter_by(question_id=q_id).first()
    topic = Topic.query.filter_by(topic_id=question.topic_id).first()
    clip_1 = Clip.query.filter_by(clip_id=question.option_1_id).first()
    clip_2 = Clip.query.filter_by(clip_id=question.option_2_id).first()
    clip_3 = Clip.query.filter_by(clip_id=question.option_3_id).first()
    clip_4 = Clip.query.filter_by(clip_id=question.option_4_id).first()

    best_option = -1
    worst_option = -1

    best_option_id = user_questions[session['curr_q_id']].best_option
    worst_option_id = user_questions[session['curr_q_id']].worst_option


    

    if best_option_id != None:
        # match to a clip, 0-
        best_option = best_option_id

    if worst_option_id != None:
        # match to a clip, 0-3
        worst_option = worst_option_id

    context = {
        'user_id': session['user_id'],
        'topic': topic.title,
        'question_id': q_id,
        'question_index': session['curr_q_id'],
        'max_questions': MAX_QUESTIONS,
        'best_option': best_option,
        'worst_option': worst_option,
        'option_1': {
            'embed_link': clip_1.embed_link + '?start=' + str(clip_1.start_time),
            'transcript': clip_1.transcript,
            # 'start_time': clip_1.start_time
        },
        'option_2': {
            'embed_link': clip_2.embed_link + '?start=' + str(clip_2.start_time),
            'transcript': clip_2.transcript,
            # 'start_time': clip_2.start_time
        },
        'option_3': {
            'embed_link': clip_3.embed_link + '?start=' + str(clip_3.start_time),
            'transcript': clip_3.transcript,
            # 'start_time': clip_3.start_time
        },
        'option_4': {
            'embed_link': clip_4.embed_link + '?start=' + str(clip_4.start_time),
            'transcript': clip_4.transcript,
            # 'start_time': clip_4.start_time
        }
    }
    # print(context)
    
    return render_template('question.html', **context)


@app.route('/api/answer_question/', methods=['POST'])
def answer_question():
    user_id = request.form.get('user_id')
    question_id = request.form.get('question_id')
    best_option = request.form.get('best_option')
    worst_option = request.form.get('worst_option')

    # if not user_id or not question_id or not best_option or not worst_option:
    #     abort(404)

    # user = User.query.get(user_id)
    # question = Question.query.get(question_id)
    # if not user or not question:
    #     abort(404)

    current_user_q = User_Question.query.filter_by(user_id=session['user_id']).filter_by(question_id=question_id).first()

    current_user_q.best_option = best_option
    current_user_q.worst_option = worst_option
    # new_answer = User_Question(user_id=user_id, question_id=question_id, best_option=best_option, worst_option=worst_option)
    # db.session.update(current_user_q)
    db.session.commit()
    
    return redirect(url_for('show_question', id='1'))

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
