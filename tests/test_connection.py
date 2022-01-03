import os
from unittest import TestCase
from unittest.mock import patch, MagicMock

from belastingen.api.belastingen.key2belastingen import K2bConnection
from . import FIXTURE_PATH


class ResponseMock:
    def json(self):
        return {"a": 1}

    @property
    def status_code(self):
        return 200

    def content(self):
        return b"{'a': 1}"


@patch("belastingen.api.belastingen.key2belastingen.requests.get")
@patch.dict(
    os.environ, {"BSN_TRANSLATIONS_FILE": f"{FIXTURE_PATH}/bsn_translations.json"}
)
class K2bConnectionTest(TestCase):
    def test_get_data(self, mocked_belasting_get: MagicMock):
        mocked_belasting_get.return_value = ResponseMock()
        connection = K2bConnection("https://localhost", "token")
        data = connection.get_data("111222333")
        self.assertEqual(data, {"a": 1})

    def test_translation(self, mocked_belasting_get: MagicMock):
        mocked_belasting_get.return_value = ResponseMock()
        connection = K2bConnection("https://localhost", "token")
        data = connection.get_data("123")

        # check if the request is made with the mapped bsn
        headers = mocked_belasting_get.call_args[1]["headers"]
        self.assertEqual(headers["subjid"], "234")

        self.assertEqual(data, {"a": 1})
