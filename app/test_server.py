import json
import os
from unittest.mock import patch

from app.auth import FlaskServerTestCase
from app.server import app

from app.config import FIXTURES_PATH


def _load_json(json_file_name):
    path = os.path.join(FIXTURES_PATH, json_file_name)
    with open(path) as fp:
        return json.load(fp)


def _get_fixture_bsn_found():
    return _load_json("has_belastingen.json")


def _get_fixture_no_bsn_found():
    return _load_json("unknown.json")


def _get_fixture_all():
    return _load_json("all_data.json")


@patch("app.server.get_K2B_api_location", lambda: "https://localhost")
@patch("app.server.get_bearer_token", lambda: "token")
class ApiTests(FlaskServerTestCase):
    app = app

    def test_status(self):
        response = self.client.get("/status/health")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["content"], "OK")

    @patch(
        "app.server.K2bConnection.get_data",
        lambda _self, bsn: _get_fixture_no_bsn_found(),
    )
    def test_get_belastingen_unknown_bsn(self):
        response = self.get_secure("/belastingen/get")

        expected_data = {
            "content": {"isKnown": False, "notifications": [], "tips": []},
            "status": "OK",
        }

        self.assertEqual(response.json, expected_data)

    @patch(
        "app.server.K2bConnection.get_data",
        lambda _self, bsn: _get_fixture_bsn_found(),
    )
    def test_get_belastingen_known(self):
        response = self.get_secure("/belastingen/get")

        expected_data = {
            "content": {"isKnown": True, "notifications": [], "tips": []},
            "status": "OK",
        }

        self.assertEqual(response.json, expected_data)

    @patch(
        "app.server.K2bConnection.get_data",
        lambda _self, bsn: _get_fixture_all(),
    )
    def test_get_all(self):
        response = self.get_secure("/belastingen/get")

        expected_data = {
            "content": {
                "isKnown": True,
                "notifications": [
                    {
                        "datePublished": "2020-01-28T13:11:51Z",
                        "description": "Er staat nog een aanslag open van u. Zorg voor tijdige betaling.",
                        "id": "belasting-4",
                        "priority": 1,
                        "title": "Betaal uw aanslagen",
                        "link": {
                            "title": "Betaal direct",
                            "to": "https://localhost/aanslagen.php",
                        },
                    }
                ],
                "tips": [
                    {
                        "datePublished": "2020-01-28T13:11:51Z",
                        "description": "Betaal gemakkelijk de gecombineerde belastingaanslag. Regel vandaag nog uw automatische incasso, dan hebt u er straks geen omkijken meer naar.",
                        "id": "belasting-5",
                        "priority": 10,
                        "title": "Automatische incasso",
                        "link": {
                            "title": "Vraag direct aan",
                            "to": "https://localhost/automatische.incasso.aanvragen.php",
                        },
                        "reason": "U krijgt deze tip omdat u nog niet via automatische incasso betaalt",
                    }
                ],
            },
            "status": "OK",
        }

        self.assertEqual(response.json, expected_data)

    def test_getvergunningen_no_header(self):
        response = self.client.get("/belastingen/get")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json, {"message": "Auth error occurred", "status": "ERROR"}
        )
