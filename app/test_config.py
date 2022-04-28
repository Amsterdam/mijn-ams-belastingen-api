import os
from unittest import TestCase
from unittest.mock import patch

from app.config import (
    get_bearer_token,
    get_bsn_translations,
    get_K2B_api_location,
    FIXTURES_PATH,
)


class ConfigTest(TestCase):
    @patch.dict(os.environ, {"K2B_API_LOCATION": "k2bapilocation"})
    def test_get_K2B_api_location(self):
        value = get_K2B_api_location()
        self.assertEqual(value, "k2bapilocation")

    @patch.dict(os.environ, {"K2B_BEARER_TOKEN": "k2bbearertoken"})
    def test_get_bearer_token(self):
        value = get_bearer_token()
        self.assertEqual(value, "k2bbearertoken")

    @patch.dict(
        os.environ,
        {"BSN_TRANSLATIONS_FILE": f"{FIXTURES_PATH}/bsn_translations_empty.json"},
    )
    def test_get_bsn_translations_empty(self):
        value = get_bsn_translations()
        self.assertEqual(value, {})

    @patch.dict(
        os.environ, {"BSN_TRANSLATIONS_FILE": f"{FIXTURES_PATH}/bsn_translations.json"}
    )
    def test_get_bsn_translations(self):
        value = get_bsn_translations()
        self.assertEqual(value, {"123": "234", "345": "456"})
