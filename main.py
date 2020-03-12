from datetime import datetime, timedelta
from nse import NSEDataExtractor

def main():
    """
    This is a Driver method.
    """
    nse_url = "https://archives.nseindia.com/content/historical/EQUITIES"
    number_of_days_to_extract_data = 30
    columns_to_include = ['SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE', 'TOTTRDQTY', 'TIMESTAMP']

    # Data extraction starts from yesterdays date, as no start date is given.
    nse_data_extractor = NSEDataExtractor(nse_url, columns_to_include, number_of_days_to_extract_data)
    nse_data_extractor.extract_data()

    # Parameters for start date.
    day = 13
    month = 3
    year = 2020
    nse_data_extractor = NSEDataExtractor(nse_url, columns_to_include, number_of_days_to_extract_data, datetime(year, month, day))
    #nse_data_extractor.extract_data()

main()
