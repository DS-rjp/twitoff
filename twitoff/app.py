'''
main application/routing file
for twitoff

RJProctor
'''

from os import getenv
from flask import Flask, render_template, request
from .models import DB, Tweet, User
import predict_user
from twitter import insert_example_users

# Note: we need a directory & subdirectory

# create a function that sets up application
def create_app():
    '''
    create and configure and instance 
    of the Flask application
    '''
    # it's just a shortcut to using the name of the package
    app = Flask(__name__)
    # configure connection to database and persist it
    app.config['SQLALCHEMY_DATABASE_URL'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # initialize database and connect application to database
    DB.init_app(app)

       
    # create a route
    @app.route('/')
    # create a function to 
    # query/filter results from database
    def root():
        # SELECT * FROM User
        Users = User.query.all()
        return render_template('base.html', title='Home',
                                users=User.query.all())
    
    # create a route
    @app.route('/user', methods='POST')
    # create a route
    @app.route('/user/<name>', methods='GET')
    # create a function to 
    # add a specific user using user input
    def user(name=None, message=' '):
        # either passing in a name or pulling it from database
        name = name or request.values('user_name')
        try:
            if request.method == 'POST'
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            # filter to the user and pull tweets
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name,tweets=tweets,
                               message=message)
    
    # create a route
    @app.route('/compare', methods='POST')
    # create a function to 
    # compare users
    def compare(message=' '):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else: 
            prediction = predict-user(user1,user2,
                                      request.values['tweet_Itext'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user2)
    return render_template('prediction.html', title='Prediction', message=message)
          
    # create a route
    @app.route('/update')
    # create a function to
    # add data to database
    def update():
        insert_example_users()  
        return render_template('base.html', title='Users updated!',
                                users=User.query.all())
     
    # create a route
    @app.route(/'reset')
    # create a function to
    # reset database
    def reset():
        # drop everthing in database
        DB.drop_all()
        # re-create the database
        DB.create_all()
        return render_templates('base.html', title='Reset database')
                
    return app






