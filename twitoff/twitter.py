'''
retrieve tweets from Twitter
and embeddings from Spacy
and persist in the database

RJProctor
'''
import Spacy
import tweepy
from .models import DB, Tweet, User
from os import getenv

TWITTER_USERS ['calebhicks', 'elonmusk', 'rrherr','SteveMartinToGo',
               'alynkovic', 'nasa', 'sadserver', 'jkholand', 'austen',
               'common_squirrel', 'KenJennings', 'conanobrian',
               'big_ben_clock', 'IAM_SHAKESPEAR']

# creates twitter object 
# authorized twitter API connection
TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

# load vectorization model
# to return string values as numpy arrays
# for use in logistic regression model
# (preprocessing)
nlp = spac.load('my_model')
def vectorized_tweet(tweet_text):
    return nlp(tweet_text).vector

# create function to add or updates a user
# and add their corresponding tweets
def add_or_update_user(username):
    '''
    add or update a user and their corresponding tweets
    return error if not a Twitter user
    (one function to serve them all)
    '''
    try:
        # define twitter user 
        twitter_user = TWITTER.get_user(username)
        # query for twitter user
        db_user = (User.query.get(twitter_user.id) or
                    # filter for user and update user
                    # if user exists (if query True)
                   User(id=twitter_user.id, name=username))
                    # instantiate new twitter user
                    # if no user exists (if query False)
        # add user to database
        DB.session.add(db_user)
    
        # pull tweets - limit to primary tweets 
        # (no retweets/reply tweets)
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id)
                # filters to unseen tweets
        
        # store newest tweet id
        if tweets:
             db_user.newest_tweet_id = tweets[0.id]

        # instantiate, append to user, and add to database
        for tweet in tweets:
            # create new column/store most recent tweet
            # with describtion of tweet in user table                                   model='twitter')
            vectorized_tweet = vectorized_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300],
                             vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
         
        # persist changes to database
        DB.session.commit()

    # create exception to handle errors
    except Exception as e:
        # returns error to end user
        print('Error processing {}: {}'.format(username, e))
        # returns error to the rest of the packages know about the exception
        raise e
    else: 
        # save changes to database
        DB.session.commit()

    # add data to database
def insert_example_users():
    # add sample data to database
    add_or_update_user('austen')
    add_or_update_user('elonmusk')
