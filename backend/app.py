from flask import Flask, redirect, request, session, render_template, render_template_string
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import google.oauth2.credentials
import pandas as pd

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['GOOGLE_CLIENT_ID'] = '960270714715-scg1n3nvl4734ld5mog1338la72kad75.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = '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'
# app.config['GOOGLE_REDIRECT_URI'] = 'http://chrome.soumit.in:5000/callback'
app.config['GOOGLE_REDIRECT_URI'] = 'http://127.0.0.1:5000/callback'
app.config['GOOGLE_SCOPES'] = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # csv file upload method
    if 'file' in request.files:
        # get the uploaded file
        file = request.files['file']

        # save the uploaded file to a directory
        file.save(os.path.join('uploads', file.filename))

        # read csv to list
        df = pd.read_csv(os.path.join('uploads', file.filename), on_bad_lines='skip', header=None)

        # save csv to session
        session['file'] = file.filename

    # csv from url
    else:
        # get the url
        url = request.form['url']

        # read csv to list
        df = pd.read_csv(url, on_bad_lines='skip', header=None)

        # save csv to local storage
        df.to_csv(f'uploads/{request.form["name"]}.csv', index=False)

        # save csv to session
        session['file'] = f'{request.form["name"]}.csv'

    name = request.form['name']
    session['name'] = name

    # start login process    
    google_flow = Flow.from_client_secrets_file(
        'client3.json',
        scopes=app.config['GOOGLE_SCOPES'],
        redirect_uri=app.config['GOOGLE_REDIRECT_URI']
    )
    authorization_url, state = google_flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    google_flow = Flow.from_client_secrets_file(
        'client3.json',
        scopes=app.config['GOOGLE_SCOPES'],
        redirect_uri=app.config['GOOGLE_REDIRECT_URI']
    )
    google_flow.fetch_token(authorization_response=request.url)

    if not google_flow.credentials:
        return 'Failed to retrieve access token.'

    credentials = google_flow.credentials
    service = build('sheets', 'v4', credentials=credentials)

    spreadsheet_body = {
        'properties': {
            'title': session.get('name')
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet_body).execute()
    spreadsheet_id = spreadsheet['spreadsheetId']

    csv = session.get('file')
    df = pd.read_csv(f'uploads/{csv}', on_bad_lines='skip', header=None)
    df = df.fillna('')
    
    # Convert DataFrame to list of lists
    values = df.values.tolist()

    os.remove(os.path.join('uploads', csv))

    # Prepare the update request
    requestt = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Sheet1!A1',
        valueInputOption='RAW',
        body={
            'values': values
        }
    )

    # Execute the update request
    create = requestt.execute()

    response = f"""
    Your CSV is now in Google Sheets!
    <br>
    <a href="https://docs.google.com/spreadsheets/d/spreadsheet_id" target="_blank">https://docs.google.com/spreadsheets/d/spreadsheet_id</a>
    """
    # return render_template_string(response.replace("spreadsheet_id", spreadsheet_id))
    return render_template('success.html', spreadsheet_id=spreadsheet_id)


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # app.run(host="0.0.0.0")
    app.run()