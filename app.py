from flask import Flask, jsonify, request
from nse import NSEDataExtractor

app = Flask(__name__)

NSE_BASE_URL = "https://archives.nseindia.com/content/historical/EQUITIES"

# get_details_of_symbol?symbol=20MICRONS&date=3/3/2020
@app.route('/get_details_of_symbol')
def get_details_of_symbol():
    """
    This method returns all the details of a given symbol on a particular date.
    """

    symbol = request.args.get('symbol', default = 'empty', type = str)
    date_to_capture = request.args.get('date', default = 'empty', type = str)
    
    if symbol == 'empty' or date_to_capture == 'empty':
        print(symbol, date_to_capture)
        return jsonify('Please provide the Symbol and a Date.'), 400

    nse_data_extractor = NSEDataExtractor(NSE_BASE_URL)
    #print(nse_data_extractor.get_data_for_symbol(symbol, date_to_capture))
    return jsonify(nse_data_extractor.get_data_for_symbol(symbol, date_to_capture)), 200
    

if __name__ == '__main__':
    app.run()