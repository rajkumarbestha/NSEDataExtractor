NSEDataExtractor
=========================
NSEDataExtractor extracts the data from National Stock Exchange.

## To Run
```
pip install requirements.txt
python main.py
``` 
to run the extraction with default values.
You can also change the date, number of days to retrieve the data and can choose the columns to consider in the csv file.

## To Start the Flask Server
```
python app.py
```
and hit localhost:5000/get_details_of_symbol?symbol=20MICRONS&date=3/3/2020 to get the details of the symbol on a particular date.
