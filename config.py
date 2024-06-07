import os
from dotenv import load_dotenv



load_dotenv()

ADMIN_ID = int(os.getenv('ADMIN_ID'))
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('channel_id')
CHANNEL_URL = os.getenv('CHANNEL_URL')