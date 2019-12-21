#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv, find_dotenv
from pathlib import *
load_dotenv(find_dotenv())
env_path = Path('.') / '../.env'

# try:
#     ENVIRONMENT = os.getenv('ENVIRONMENT')
#     if ENVIRONMENT is None:
#         raise Exception('ENVIRONMENT is not set')
# except Exception as e:
#     print(e)
#     ENVIRONMENT = 'development'


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundoo.setting.production')
    print("manage.py")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
