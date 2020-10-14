'''
SQLALchemy models/schema and utility functions
for TwitOff
(the database)

RJProctor
'''
from flask_sqlalchemy import SQLAlchemy

# instantiate a database 
DB = SQLAlchemy()

# create class with inheritance from DB.Model
class User(DB.Model):
    '''
    Twitter users corresponding to Tweets
    '''
    id = DB.Columnn(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String,(15), nullable=False)
    # Tweet IDs are ordinal integers
    # they can be used to fetch only more recent
    newest_tweet_id = DB.Column(DB.BigInterger)

    # define representation method
    # for presentation clarification
    def __repr__(self):
        return '-User {}-'.format(self.name)

class Tweet(DB.Model):
    '''
    Tweets, text, and data
    '''
    # Note: migration wil allow you to change schema
    # without throwing out data but we won't cover that 
    # yet - we will jsut recreate the DB
    id = DB.Columnn(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode,(300)) 
        # allows for text plus links
    embedding = DB.Column(DB.PickleType, nullable=False)
        # transforms from text to numeric objects - serializes strings
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
        # relational database, connects data from this table
        # to user table; works in combination with line below
        # required field
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
        # backreference keeps you from having to explicitly join

    # define representation method
    # for presentation clarification
    def __repr__(self):
        return '-Tweet {}-'.format(self.text)

# # add data to database
# def insert_example_users():
#     # create sample data
#     austen = User(id=1, name='austen')
#     elon = User(id=2, name='elonmusk')
#     # add sample data to database
#     DB.session.add(austen)
#     DB.session.add(elon)
#         # this should be a for loop
#         #for user in insert_example_users:
#             #return DB.session.add(user)
#     # save changes to database (persist changes)
#     DB.session.commit()

# def insert_example_tweets():
#     # create sample data
#     tweet1 = Tweet(id = 1, text='Two more Lambda School students just got hired!', user_id= 1 , user='austen' )
#     tweet2 = Tweet(id = 2, text='Another Awesome Build Week! Great work everyone.', user_id= 1, user='austen' )
#     tweet3 = Tweet(id = 3, text='Lambda School is the Best!', user_id= 1, user='austen' )
#     tweet4 = Tweet(id = 4, text='SpaceX is the Best!', user_id= 2, user='elonmusk' )
#     tweet5 = Tweet(id = 5, text='Great news from Tesla...', user_id= 2, user='elonmusk' )
#     tweet6 = Tweet(id = 6, text='On the journey to Mars...', user_id= 2, user='elonmusk' )
#     # add sample data to database
#     DB.session.add(tweet1)
#     DB.session.add(tweet2)
#     DB.session.add(tweet3)
#     DB.session.add(tweet4)
#     DB.session.add(tweet5)
#     DB.session.add(tweet6)
#         # this should be a for loop
#         #for tweet in insert_example_tweets:
#             #return DB.session.add(tweet)
#     # save changes to database (persist changes)
#     DB.session.commit()

