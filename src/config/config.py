import os

API_URL = os.environ.get('API_URL')
MIN_SLEEP_TIME = int(os.environ.get('MIN_TIME_SLEEP'))
MAX_SLEEP_TIME = int(os.environ.get('MAX_TIME_SLEEP'))
TABLE_ID = os.environ.get("TABLE_ID")
RESERVATION_AMOUNT = int(os.environ.get("RESERVATION_AMOUNT"))
NUMBER_OF_PERIODS = int(os.environ.get("NUMBER_OF_PERIODS"))
INTEREST_RATE = float(os.environ.get("INTEREST_RATE"))

MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_DB = os.environ.get('MONGODB_DB')
MONGODB_USERS_COLLECTION = os.environ.get('MONGODB_USERS_COLLECTION')
MONGODB_SETTINGS_COLLECTION = os.environ.get('MONGODB_SETTINGS_COLLECTION')