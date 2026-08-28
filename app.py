from flask import Flask
from backtest import backtest_bp

app = Flask(app.register_blueprint(backtest_bp)
_)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
