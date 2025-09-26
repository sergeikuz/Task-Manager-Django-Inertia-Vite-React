"""
Test settings for Django tests
"""

from pathlib import Path

from backend.settings import *  # noqa: F403 F401

# Define BASE_DIR similar to main settings
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Fixed SECRET_KEY for tests
SECRET_KEY = 'django-insecure-test-key-for-running-tests-only'

# Disable DEBUG for tests
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable Rollbar for tests
ROLLBAR = {
    'access_token': 'test_token',
    'environment': 'test',
    'code_version': '1.0',
    'root': BASE_DIR,
}
