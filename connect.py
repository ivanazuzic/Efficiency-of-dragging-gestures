import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def connect():
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)

    # authorize the clientsheet
    client = gspread.authorize(creds)
    sheet = client.open("Efficiency of dragging gestures - log").sheet1 # open sheet
    return sheet
