from datetime import datetime, timedelta
import requests, zipfile, io
import pandas as pd

class NSEDataExtractor:
    """
    This Class deals with data extraction from NSE.
    If no start date is given, Data extraction starts from yesterday's date.
    """

    def __init__(self, url_to_get_data, columns_needed = [], data_for_number_of_days = 30, start_date = datetime.now()):
        # Strip to remove accidental whitespaces.
        self.url_to_get_data = url_to_get_data.strip()
        self.columns_needed  = columns_needed
        self.data_for_number_of_days = data_for_number_of_days
        self.start_date = start_date


    def construct_url_for_date(self, date_to_capture):
        """
        This method constructs the NSE url to get the zip file.
        """

        date_to_string = date_to_capture.strftime('%d%b%Y').upper()
        url = self.url_to_get_data + '/' + date_to_string[-4:] + '/' + date_to_string[-7:-4] + '/cm' + date_to_string + 'bhav.csv.zip'
        return url


    def get_zip_file(self, url):
        """
        This method hits NSE and returns the Zip File.
        This method can also be used by other classes to get a ZipFile from any URL.
        """

        req = requests.get(url)
        zip = zipfile.ZipFile(io.BytesIO(req.content))
        return zip


    def save_required_info(self, zip, file_name):
        """
        This method takes the zip file and saves the required columns in a differemt file.
        """

        df = pd.read_csv(zip.open('cm'+file_name))
        df[self.columns_needed].to_csv ('cm'+file_name, index = False, header=True)


    def extract_data(self):
        """
        This method is a driver which accomplishes the given task by using above methods efficiently.
        """

        for i in range(self.data_for_number_of_days):
            try:
                date_to_capture = self.start_date - timedelta(i+1)

                # Checking for Non-Week Days.
                if date_to_capture.weekday() not in (5, 6):

                    # Get URL.
                    url = self.construct_url_for_date(date_to_capture)
                    print(url)

                    # Get ZipFile.
                    zip = self.get_zip_file(url)

                    # Open Zip and save required information.
                    self.save_required_info(zip, date_to_capture.strftime('%d%b%Y').upper()+'bhav.csv')

            # If the current date is a holiday, there'll be no data with NSE. So, the URL times out.
            except:
                print(date_to_capture.strftime('%d%b%Y').upper(), "is a holiday. So, No data in NSE.")


    def get_data_for_symbol(self, symbol, date_to_capture):
        """
        This method is a driver used by the flask app to get the details of the symbol on a particular date.
        """

        date_to_capture = datetime(int(date_to_capture.split('/')[-1]), int(date_to_capture.split('/')[1]), int(date_to_capture.split('/')[0]))

        try:
            # Get URL.
            url = self.construct_url_for_date(date_to_capture)
            print(url)

            # Get ZipFile.
            zip = self.get_zip_file(url)

            # Get data from csv in zip.
            data = pd.read_csv(zip.open('cm'+date_to_capture.strftime('%d%b%Y').upper()+'bhav.csv'))
            return data[data.SYMBOL.str.contains(symbol,case=False)].to_dict()
        except:
            return "No Data in NSE."



# If running as a file, rather than an import, then instantiate and test.
if __name__ == "__main__":
    nse = NSEDataExtractor("https://archives.nseindia.com/content/historical/EQUITIES", ['SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE', 'TOTTRDQTY', 'TIMESTAMP'], 30)
    nse.extract_data()



