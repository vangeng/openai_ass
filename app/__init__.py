import os
from flask import Flask
from flask.cli import load_dotenv

from .routes import assistant_bp

app = Flask(__name__)



app.register_blueprint(assistant_bp)