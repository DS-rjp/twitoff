'''
entry point for TwitOff

RJProctor
'''

# create an application
from .app import create_app

APP = create_app()

# FLASK_APP=twitoff flask run

