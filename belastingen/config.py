import json
import os
import os.path


BASE_PATH = os.path.abspath(os.path.dirname(__file__))


def get_sentry_dsn():
    return os.getenv('SENTRY_DSN', None)


def get_tma_certificate():
    tma_cert_location = os.getenv('TMA_CERTIFICATE')
    with open(tma_cert_location) as f:
        return f.read()


def get_K2B_api_location():
    return os.getenv('K2B_API_LOCATION').strip()


def get_bearer_token():
    return os.getenv('K2B_BEARER_TOKEN').strip()


def get_bsn_translations():
    file = os.getenv('BSN_TRANSLATIONS_FILE').strip()
    with open(file) as fp:
        data = json.load(fp)
    return data
