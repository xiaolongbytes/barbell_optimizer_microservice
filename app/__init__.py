from flask import Flask

app = Flask(__name__)

from app import routes

# Flask application will listen on default port when in terminal I run:
# export FLASK_APP=barbell_microservice.py
# flask run
