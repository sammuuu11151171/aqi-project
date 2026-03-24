from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import pandas as pd
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Load ML model
model = pickle.load(open('backend/model.pkl', 'rb'))

# Load dataset
df = pd.read_csv('backend/data.csv')

# ------------------ FRONTEND ROUTES ------------------

@app.route('/')
def home():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

# ------------------ API ROUTES ------------------

# Prediction API
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['data']
    result = model.predict([data])[0]

    # AQI Category
    if result <= 50:
        category = "Good"
    elif result <= 100:
        category = "Satisfactory"
    elif result <= 200:
        category = "Moderate"
    elif result <= 300:
        category = "Poor"
    else:
        category = "Hazardous"

    return jsonify({
        "aqi": int(result),
        "category": category
    })


# Insights API
@app.route('/insights')
def insights():
    avg_aqi = int(df['AQI'].mean())
    max_city = df.groupby('City')['AQI'].mean().idxmax()

    return jsonify({
        "average_aqi": avg_aqi,
        "most_polluted_city": max_city
    })


# Trend API
@app.route('/trend')
def trend():
    trend_data = df.groupby('Date')['AQI'].mean().reset_index()

    return jsonify(trend_data.to_dict(orient='records'))


# ------------------ RUN ------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
