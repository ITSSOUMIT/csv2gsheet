# csv2gsheet
A chrome extension + python flask app, to import any csv to google sheets.

Features -
1. Upload CSV to import to Google Sheets.
2. Insert CSV link, to import to Google Sheets.

Usage -
1. Clone the repository
2. In chrome browser, open [chrome://extensions](chrome://extensions)
3. Turn on Developer mode
4. Click `Load unpacked` and select the `chrome-extension` folder
5. `csv2gsheet v1.0` extension will be added to chrome.


[OPTIONAL]
This is also an independent **python flask app**, which can be used to import csv to google sheets.
To use the flask app, follow the steps -
1. Clone the repository
2. Go to the backend folder
3. Install the requirements using `pip install -r requirements.txt`
4. For Mac/Linux based systems, change permission of uploads folder : `sudo chmod -R 777 uploads/`
5. Run using `python app.py`
6. The app will be running on `http://localhost:5000/`

#### Direct server link, for chrome extension's backend -
[http://chrome.soumit.in:5000](http://chrome.soumit.in:5000)