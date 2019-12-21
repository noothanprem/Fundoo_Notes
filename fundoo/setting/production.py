from .base import *
from .testing import *
from .development import *
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR, "Base directoryy")
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY')




CORS_ORIGIN_ALLOW_ALL = False



SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api-key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}








