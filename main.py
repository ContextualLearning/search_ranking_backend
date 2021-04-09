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
