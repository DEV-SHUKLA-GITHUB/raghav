from flask import Flask, jsonify, request
from nselib import derivatives
import pandas as pd
from flask_cors import CORS
import logging
import os

app = Flask(__name__)

# Enable CORS for your local frontend
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Set up logging for diagnostics
logging.basicConfig(level=logging.INFO)

@app.after_request
def after_request(response):
    # Ensure CORS headers are present on all responses
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def index():
    return 'Backend is running!', 200

@app.route('/api/premium-traded')
def premium_traded():
    date = request.args.get('date', '07-07-2025')
    # Convert date from yyyy-mm-dd to dd-mm-yyyy
    try:
        year, month, day = date.split('-')
        formatted_date = f"{day}-{month}-{year}"
    except Exception as e:
        app.logger.error(f"Date parsing error: {e}")
        formatted_date = '07-07-2025'

    try:
        data = derivatives.fno_bhav_copy(formatted_date)
        # Check if expected columns exist
        required_cols = {'OptnTp', 'TtlTradgVol', 'SttlmPric', 'NewBrdLotQty', 'TckrSymb'}
        if data.empty or not required_cols.issubset(data.columns):
            app.logger.warning(f"Data not available or missing columns for date {formatted_date}")
            return jsonify({"error": "Data not available for this date"}), 404

        filtered_data = data[data['OptnTp'].isin(['PE', 'CE'])]
        filtered_data.loc[:, 'Premium Traded'] = (
            filtered_data['TtlTradgVol'] * filtered_data['SttlmPric'] * filtered_data['NewBrdLotQty']
        )
        grouped_data = filtered_data.groupby('TckrSymb')['Premium Traded'].sum().reset_index()
        grouped_data = grouped_data.sort_values(by='Premium Traded', ascending=False)
        grouped_data['Premium Traded (Crores)'] = grouped_data['Premium Traded'] / 10_000_000
        ab = grouped_data[['TckrSymb', 'Premium Traded (Crores)']]
        return jsonify(ab.to_dict(orient='records'))
    except Exception as e:
        app.logger.error(f"Error in /api/premium-traded: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)