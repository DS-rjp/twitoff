'''
Mininal example Flask application

RJProctor
'''
from flask import Flask

# set up an application
app = Flask(__name__)

# set up a route  
# listens for commands/sends responses
@app.rout('/')

# create a function
def hello_world():
    return 'Hello, World! '
