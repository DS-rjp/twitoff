'''
main application/routing file
for twitoff

RJProctor
'''

from os import getenv
from pickle import dumps, loads
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, Tweet, User
from .predict import predict_user
from twitter import add_or_update_user, update_all_users

# Note: we need a directory & subdirectory

load_dotenv()

if getenv('FLASK_ENV') == 'production':
    from redis import redis
    CACHE = Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'),
                  pasword=config('REDIS_PASWORD'))
else:        # development/test, use local mocked REDIS
    from birdisle.redis import Redis
    CACHE = Redis()

CACHED_COMPARISONS = (loads(CACHE.get('comparisons'))
                      if CACHE.exits('comparisons') else set())


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
                                users=User.query.all(), 
                                comparisons=CACHED_COMPARISONS)
    
    # create a route
    # for end user through form submission
    @app.route('/user', methods='POST')
    # create a route
    # access database by twitter user name
    @app.route('/user/<name>', methods='GET')
    # create a function to 
    # add a specific user using end user input
    def user(name=None, message=' '):
        # either passing in a name or pulling it from database
        name = name or request.values('user_name')
        try:
            # if end user completes a form submission...
            # the following will occur
            if request.method == 'POST'
                # from .twitter.py
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            # filter to the user and pull tweets 
            # associated with specific user
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            # if an error occurs
            # return a message to end user that includes
            # the name of the twitter user and the error
            message = 'Error adding {}: {}'.format(name, e)
            # cast tweets as 0; there are no tweets for a
            # user that does not exist
            tweets = []
        return render_template('user.html', title=name,tweets=tweets,
                               message=message)
    
    # create a route
    @app.route('/compare', methods='POST')
    # create a function to 
    # compare users using end user input
    def compare(message=' '):
        # add sorted users
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else: 
            prediction = predict_user(user1, user2,
                                      request.values['tweet_text'], 
                                      CACHE)
            CACHED_COMPARISONS.add((user1, user2))
            CACHE.set('comparisons', dumps(CACHED_COMPARISONS))
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user2)
        return render_template('prediction.html', title='Prediction', 
                               message=message)
          
    # create a route
    @app.route('/update')
    # create a function to
    # add data to database
    def update():
        CACHE.flushall()
        CACHED_COMPARISONS.clear()
        insert_example_users()  
        return render_template('base.html', title='Users updated!',
                                users=User.query.all())
     
    # create a route
    @app.route(/'reset')
    # create a function to
    # reset database
    def reset():
        CACHE.flushall()
        CACHED_COMPARISONS.clear()
        # drop everthing in database
        DB.drop_all()
        # re-create the database
        DB.create_all()
        return render_templates('base.html', title='Reset database')
                
    return app






