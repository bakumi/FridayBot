import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
CHANNEL_URL = os.getenv('CHANNEL_URL')
ADMIN_ID = list(map(int, os.getenv('ADMIN_ID').split(',')))
