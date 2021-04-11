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
        session['curr_q_id'] = 0
        return redirect(url_for('show_question', id=str(session['curr_q_id'])))

    return render_template('login.html')

@app.route('/new_user/', methods=['POST', 'GET'])
def new_user():

    uniqname = request.form.get('uniqname')
    print(uniqname)
    if not uniqname:
        abort(404)

    user = User.query.filter_by(uniqname=uniqname).first()

    if user:
        session['user_id'] = user.user_id
        session['curr_q_id'] = 0
        return redirect(url_for('show_question',id=str(session['curr_q_id'])))

    new_user = User(uniqname=uniqname)
    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)

    # 1. generate the questions
    # 2. for each questions, add to use_question table without best and worst option

    question = get_questions()


    for i in question:
      user_id = new_user.user_id
      question_id = i['question_id']
      best_option = None
      worst_option = None
      new_answer = User_Question(user_id=user_id, question_id=question_id, best_option=best_option, worst_option=worst_option)
      db.session.add(new_answer)
      db.session.commit()

    session['user_id'] = new_user.user_id
    session['annotate'] = 0

    return redirect(url_for('show_question',id=str(0)))

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

    session['annotate'] = len([u_q.question_id for u_q in user_questions if (u_q.best_option != None and u_q.worst_option != None)])

    session['curr_q_id'] = int(id)
    print(session['curr_q_id'])

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

    best_option_asc = None
    worst_option_asc = None

    

    if best_option_id != None:
        # match to a clip, 0-
        best_option = best_option_id
        best_option_asc = chr(best_option + 64)

    if worst_option_id != None:
        # match to a clip, 0-3
        worst_option = worst_option_id
        worst_option_asc = chr(worst_option + 64)


    context = {
        'user_id': session['user_id'],
        'topic': topic.title,
        'question_id': q_id,
        'annotation':session['annotate'],
        'question_index': session['curr_q_id'],
        'cur_id':session['curr_q_id'] + 1,
        'max_questions': MAX_QUESTIONS,
        'best_option': best_option,
        'worst_option': worst_option,
        'best_option_asc': best_option_asc,
        'worst_option_asc': worst_option_asc,
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

    curent_index = request.form.get('id')

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

    # session['annotate'] = int(request.form.get('annotation'))
    session['annotate'] = min(int(request.form.get('annotation')), session['curr_q_id'] + 1)
    if session['annotate'] == 18:
        print(1)
        return redirect(url_for('contextlearning'))
    else:
        return redirect(url_for('show_question', id=str(curent_index)))

# @app.route('/new_user/', methods=['POST', 'GET'])
@app.route('/contextlearning/', methods = ['GET'])
def contextlearning():
    return render_template('finish.html')