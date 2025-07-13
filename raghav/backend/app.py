from flask import Flask, jsonify, request
from nselib import derivatives
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/premium-traded')
def premium_traded():
    date = request.args.get('date', '07-07-2025')
    # Convert date from yyyy-mm-dd to dd-mm-yyyy
    try:
        day, month, year = date.split('-')[2], date.split('-')[1], date.split('-')[0]
        formatted_date = f"{day}-{month}-{year}"
    except Exception:
        formatted_date = '07-07-2025'

    data = derivatives.fno_bhav_copy(formatted_date)
    filtered_data = data[data['OptnTp'].isin(['PE', 'CE'])]
    filtered_data.loc[:, 'Premium Traded'] = (
        filtered_data['TtlTradgVol'] * filtered_data['SttlmPric'] * filtered_data['NewBrdLotQty']
    )
    grouped_data = filtered_data.groupby('TckrSymb')['Premium Traded'].sum().reset_index()
    grouped_data = grouped_data.sort_values(by='Premium Traded', ascending=False)
    grouped_data['Premium Traded (Crores)'] = grouped_data['Premium Traded'] / 10_000_000
    ab = grouped_data[['TckrSymb', 'Premium Traded (Crores)']]
    return jsonify(ab.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)
