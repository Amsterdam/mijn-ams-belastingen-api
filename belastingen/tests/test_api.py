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
    HAS_BELASTINGEN_BSN = '111222333'
    NO_BELASTINGEN_BSN = '123456782'

    def setUp(self):
        """ Setup app for testing """
        self.client = self.get_tma_test_app(app)

    def test_health(self):
        response = self.client.get('/status/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"OK")

    @patch('belastingen.server.K2bConnection.get_data', lambda _self, bsn: _get_fixture_no_bsn_found())
    def test_get_belastingen_unknow_bsn(self):
        SAML_HEADERS = self.add_digi_d_headers(self.NO_BELASTINGEN_BSN)

        response = self.client.get('/belastingen/get', headers=SAML_HEADERS)

        expected_data = {
            'content': {
                'data': [],
                'status': 'BSN unknown'
            },
            'status': 'OK'
        }

        self.assertEqual(response.json, expected_data)

    @patch('belastingen.server.K2bConnection.get_data', lambda _self, bsn: _get_fixture_bsn_found())
    def test_get_belastingen(self):
        SAML_HEADERS = self.add_digi_d_headers(self.HAS_BELASTINGEN_BSN)

        response = self.client.get('/belastingen/get', headers=SAML_HEADERS)

        expected_data = {
            'content': {
                'data': [
                    {
                        'categorie': 'F2',
                        'datum': '2020-01-28T10:07:18Z',
                        'nummer': 1,
                        'omschrijving': 'Themategel belastingen.',
                        'prioriteit': 0,
                        'thema': 'Belastingen',
                        'titel': 'Belastingen',
                        'url': 'https://example.com/subject.gegevens.php',
                        'url_naam': 'Belastingen'
                    }
                ],
                'status': 'BSN known'
            },
            'status': 'OK'
        }

        self.assertEqual(response.json, expected_data)

    @patch('belastingen.server.K2bConnection.get_data', lambda _self, bsn: _get_fixture_all())
    def test_get_all(self):
        SAML_HEADERS = self.add_digi_d_headers(self.HAS_BELASTINGEN_BSN)

        response = self.client.get('/belastingen/get', headers=SAML_HEADERS)

        expected_data = {
            'content': {
                'data': [
                    {
                        'categorie': 'F2',
                        'datum': '2020-01-28T13:11:51Z',
                        'nummer': 1,
                        'omschrijving': 'Themategel belastingen.',
                        'prioriteit': 0,
                        'thema': 'Belastingen',
                        'titel': 'Belastingen',
                        'url': 'https://example.com/subject.gegevens.php',
                        'url_naam': 'Belastingen'
                    },
                    {
                        'categorie': 'M1',
                        'datum': '2020-01-28T13:11:51Z',
                        'nummer': 4,
                        'omschrijving': 'Er staat nog een aanslag open van u. '
                                        'Zorg voor tijdige betaling.',
                        'prioriteit': 1,
                        'thema': 'Belastingen',
                        'titel': 'Betaal uw aanslagen',
                        'url': 'https://example.com/aanslagen.php',
                        'url_naam': 'Betaal direct'
                    },
                    {
                        'categorie': 'M2',
                        'datum': '2020-01-28T13:11:51Z',
                        'nummer': 5,
                        'omschrijving': 'Betaal gemakkelijk de gecombineerde '
                                        'belastingaanslag. Regel vandaag nog uw '
                                        'automatische incasso, dan hebt u er '
                                        'straks geen omkijken meer naar.',
                        'prioriteit': 10,
                        'thema': 'Belastingen',
                        'titel': 'Automatische incasso',
                        'url': 'https://example.com/automatische.incasso.aanvragen.php',
                        'url_naam': 'Vraag direct aan'
                    }
                ],
                'status': 'BSN known'
            },
            'status': 'OK'
        }

        self.assertEqual(response.json, expected_data)
