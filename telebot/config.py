import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
PATH_TO_DB = os.getenv('PATH_TO_DB')