import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from db import db
from models import *

# Define 'app' here FIRST before registering blueprints
app = Flask(__name__)

# Now it is completely safe to load and register blueprints
from bt_engine import backtest_bp
app.register_blueprint(backtest_bp)

from scan import scan_bp

@app.route('/')
def home():
    return "🚀 Trillion Engine Team is Active and Online!"
