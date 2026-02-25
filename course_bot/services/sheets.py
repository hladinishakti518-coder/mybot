import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_SHEET_ID
import logging

SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]


def add_user_to_sheet(user_data):
    """
    user_data: dict {
        'date': '2023-10-01',
        'tg_id': 123456,
        'username': '@user',
        'email': 'user@mail.ru',
        'phone': '+7999...',
        'amount': 5000,
        'end_date': '2024-01-01'
    }
    """
    try:
        creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

        row = [
            user_data['date'],
            str(user_data['tg_id']),
            user_data['username'],
            user_data['email'],
            user_data['phone'],
            str(user_data['amount']),
            user_data['end_date']
        ]

        sheet.append_row(row)
        logging.info(f"User {user_data['tg_id']} added to Google Sheet")
        return True
    except Exception as e:
        logging.error(f"Error adding to Google Sheet: {e}")
        return False
