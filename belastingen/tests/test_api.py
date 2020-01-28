import json
import os
from unittest.mock import patch

from tma_saml import FlaskServerTMATestCase
from tma_saml.for_tests.cert_and_key import server_crt

from belastingen.config import BASE_PATH
from belastingen.server import app

FIXTURE_PATH = os.path.join(BASE_PATH, 'tests', 'fixtures')


def _load_json(json_file_name):
    path = os.path.join(FIXTURE_PATH, json_file_name)
    with open(path) as fp:
        return json.load(fp)


def _get_fixture_bsn_found():
    return _load_json('has_belastingen.json')


def _get_fixture_no_bsn_found():
    return _load_json('unknown.json')


def _get_fixture_all():
    return _load_json('all_data.json')


@patch("belastingen.server.get_tma_certificate", lambda: server_crt)
class ApiTests(FlaskServerTMATestCase):
    TEST_BSN = '111222333'

    def setUp(self):
        """ Setup app for testing """
        self.client = self.get_tma_test_app(app)

    def test_health(self):
        response = self.client.get('/status/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"OK")

    @patch('belastingen.server.K2bConnection.get_data', lambda _self, bsn: _get_fixture_no_bsn_found())
    def test_get_belastingen_unknown_bsn(self):
        SAML_HEADERS = self.add_digi_d_headers(self.TEST_BSN)

        response = self.client.get('/belastingen/get', headers=SAML_HEADERS)

        expected_data = {
            'content': {
                'isKnown': False,
                'meldingen': [],
                'tips': []
            },
            'status': 'OK'
        }

        self.assertEqual(response.json, expected_data)

    @patch('belastingen.server.K2bConnection.get_data', lambda _self, bsn: _get_fixture_bsn_found())
    def test_get_belastingen_known(self):
        SAML_HEADERS = self.add_digi_d_headers(self.TEST_BSN)

        response = self.client.get('/belastingen/get', headers=SAML_HEADERS)

        expected_data = {
            'content': {
                'isKnown': True,
                'meldingen': [],
                'tips': []
            },
            'status': 'OK'
        }

        self.assertEqual(response.json, expected_data)

    @patch('belastingen.server.K2bConnection.get_data', lambda _self, bsn: _get_fixture_all())
    def test_get_all(self):
        SAML_HEADERS = self.add_digi_d_headers(self.TEST_BSN)

        response = self.client.get('/belastingen/get', headers=SAML_HEADERS)

        expected_data = {
            'content': {
                'isKnown': True,
                'meldingen': [
                    {
                        'datePublished': '2020-01-28T13:11:51Z',
                        'description': 'Er staat nog een aanslag open van u. Zorg voor tijdige betaling.',
                        'id': 4,
                        'priority': 1,
                        'title': 'Betaal uw aanslagen',
                        'url': {
                            'title': 'Betaal direct',
                            'url': 'https://example.com/aanslagen.php'
                        }
                    }
                ],
                'tips': [
                    {
                        'datePublished': '2020-01-28T13:11:51Z',
                        'description': 'Betaal gemakkelijk de gecombineerde belastingaanslag. Regel vandaag nog uw automatische incasso, dan hebt u er straks geen omkijken meer naar.',
                        'id': 5,
                        'priority': 10,
                        'title': 'Automatische incasso',
                        'url': {
                            'title': 'Vraag direct aan',
                            'url': 'https://example.com/automatische.incasso.aanvragen.php'
                        }
                    }
                ]
            },
            'status': 'OK'
        }

        self.assertEqual(response.json, expected_data)
