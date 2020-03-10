import os
from unittest import TestCase
from unittest.mock import patch


from belastingen.config import get_sentry_dsn, get_tma_certificate, get_K2B_api_location, get_bearer_token, \
    get_bsn_translations
from belastingen.tests import FIXTURE_PATH


class ConfigTest(TestCase):

    @patch.dict(os.environ, {'SENTRY_DSN': 'sentrydsn'})
    def test_get_sentry_dsn(self):
        value = get_sentry_dsn()
        self.assertEqual(value, 'sentrydsn')

    @patch.dict(os.environ, {'TMA_CERTIFICATE': __file__})
    def test_get_tma_certificate(self):
        value = get_tma_certificate()
        with open(__file__, 'r') as fp:
            self.assertEqual(value, fp.read())

    @patch.dict(os.environ, {'K2B_API_LOCATION': 'k2bapilocation'})
    def test_get_K2B_api_location(self):
        value = get_K2B_api_location()
        self.assertEqual(value, 'k2bapilocation')

    @patch.dict(os.environ, {'K2B_BEARER_TOKEN': 'k2bbearertoken'})
    def test_get_bearer_token(self):
        value = get_bearer_token()
        self.assertEqual(value, 'k2bbearertoken')

    @patch.dict(os.environ, {'BSN_TRANSLATIONS_FILE': f'{FIXTURE_PATH}/bsn_translations_empty.json'})
    def test_get_bsn_translations(self):
        value = get_bsn_translations()
        self.assertEqual(value, {})

    @patch.dict(os.environ, {'BSN_TRANSLATIONS_FILE': f'{FIXTURE_PATH}/bsn_translations.json'})
    def test_get_bsn_translations(self):
        value = get_bsn_translations()
        self.assertEqual(value, {'123': '234', '345': '456'})
