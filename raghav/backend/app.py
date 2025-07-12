from flask import Flask, jsonify
from nselib import derivatives
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/premium-traded')
def premium_traded():
    data = derivatives.fno_bhav_copy("07-07-2025")
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
    app.run(debug=True)
