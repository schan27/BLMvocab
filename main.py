import os
import pickle
import pandas as pd
from flask import Flask, render_template
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


app = Flask(__name__)

REPO_NAME = "BLMvocab"
FREEZER_BASE_URL = "http://localhost/{0}".format(REPO_NAME)
SPREADSHEET_ID = "1IyUen-aRQJdoDZN-uzKVByqe6RYNyfTQifotFCgIBDY"
RANGE = "Sheet1!A:Z"  # entire sheet

app.config['FREEZER_BASE_URL'] = FREEZER_BASE_URL

def get_data():
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    rows = result.get('values', [])

    header = rows[0]
    rows = rows[1:]
    # pad rows with values

    for i, row in enumerate(rows):
        if len(row) < len(header):
            padding = [""] * (len(header)-len(row))
            rows[i] += padding
        
        for i, el in enumerate(row):
            if not el: # empty cell
                continue 
            
            if i <= 3:
                continue 

            row[i] = el.lower()
            
    
    # TODO: sort vocabulary items by topic
    return rows, header


@app.route('/')
def hello_world():
    rows, header = get_data()
    return render_template('main.html', header=header, rows=rows)


if __name__ == "__main__":
    # Testing 
    get_data()  