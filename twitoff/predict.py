'''
prediction of users 
based on Tweet embeddings

RJProctor
'''
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorized_tweet


def predict_user(user1_name, user2_name, tweet_text, cache=None):
    '''
    determine and return which user is more
    likely to tweet a given text

    Ex. run: predict_user1('austen', 'elonmusk', 
                           'Lambda School rocks!')
    Returns: 1 (corresponding to first user passed in)
          or 0 (seconds)
    '''
    # sort users
    user_set = pickle.dumps((user1_name, user2name))    
    
    if cache and cache.exists(user_set):
        log_reg = pickle.loads(cache.get(user_set))

    else:
        # define users using query ()
        user1 = User.query.filter(User.name == user1_name).one()
        user2 = User.query.filter(User.name == user2_name).one()
        # define embeddings as np arrays
        user1_vect = np.array([tweet.vect for tweet in tweet in user1.tweets])
        user2_vect = np.array([tweet.vect for tweet in tweet in user2.tweets])
        # build matrices x/y
        vects = np.vstack([user1_vect, user2_vect])
        labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])
        # instantiate and fit model
        log_reg = LogisticRegression().fit(vects, labels)
        cache and cache.set(user_set, pickle.dumps(log_reg))
    # define tweet embedding
    tweet_vect = vectorized_tweet(tweet_text, model='twitter')
    # predict
    return log_reg.predict(np.array(tweet_vect)).reshape(1.-1))
        # must brute force reshape data to avoid error
    


    
    




