#    _|_
#   /@-@\ Copyright © OpsBeacon, Inc.
#   \ - /    All rights reserved.
#    };{

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


def get_credentials_from_account_info(service_account_info):

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    return service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES)

def clear_sheet(spreadsheet_id, sheet_id, credentials):
    """Clears the given sheet in the spreadsheet"""
    try:
        service = discovery.build('sheets', 'v4', credentials=credentials)

        requests = []

        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': sheet_id
                },
                'fields': 'userEnteredValue'
            }
        })

        body = {
            'requests': requests
        }
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body).execute()

        return response

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def import_values(spreadsheet_id, values, credentials):
    """Imports the given values into the spreadsheet"""
    try:
        service = discovery.build('sheets', 'v4', credentials=credentials)

        body = {
            'value_input_option': 'USER_ENTERED',
            'data': {
                "majorDimension": "ROWS",
                "range": "A:ZZ",
                'values': values
            }
        }

        response = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body).execute()

        return response

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
