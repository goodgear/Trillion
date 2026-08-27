from flask import Flask, render_template, jsonify
from engines.mag import mag_engine
from core.core import core_engine
from armac.parse_armac import parse_armac

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['GET'])
def predict():
    mag_signal = mag_engine()
    core_signal = core_engine()
    armac_data = parse_armac()
    result = {
        "mag_signal": mag_signal,
        "core_signal": core_signal,
        "armac_data": armac_data
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
