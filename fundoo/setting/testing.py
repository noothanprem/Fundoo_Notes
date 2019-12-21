from .base import *
from dotenv import load_dotenv, find_dotenv
from pathlib import *
try:
    from .base import *
except ImportError:
    print("Import error")

TEST_TOKEN = os.getenv('TEST_TOKEN')