import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

#path to news db
PATH_TO_DB = os.getenv('PATH_TO_DB')

#path to session manager db
PATH_TO_SM_DB = os.getenv('PATH_TO_SM_DB')


NEWS_LIMIT_PER_PAGE = 10
