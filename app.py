from flask import Flask
from db import db
from models import *
from backtest import backtest_bp
from scan import scan_bp

app.register_blueprint(scan_bp)


app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://<YOUR_RAILWAY_CONNECTION_STRING>"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Blueprints
app.register_blueprint(backtest_bp)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trillion</title>
        <style>
            body { font-family: Arial; background: #f5f5f5; padding: 40px; }
            .box { background: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: auto; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Trillion is Online</h1>
            <p>Your deployment is working.</p>
        </div>
    </body>
    </html>
    """

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
