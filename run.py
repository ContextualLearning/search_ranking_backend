from app import app
import os

# def application(environ, start_response):
#     app.run(debug=False)

if __name__ == '__main__':
    app.run(debug=True)
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # app.run(debug=True, ssl_context='adhoc')
