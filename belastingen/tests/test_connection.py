from unittest import TestCase
from unittest.mock import patch

from belastingen.api.belastingen.key2belastingen import K2bConnection


class ResponseMock:
    def json(self):
        return {'a': 1}


class K2bConnectionTest(TestCase):

    @patch('belastingen.api.belastingen.key2belastingen.requests.get', lambda *args, **kwargs: ResponseMock())
    def test_get_data(self):
        connection = K2bConnection('https://localhost', 'token')
        data = connection.get_data('111222333')
        self.assertEqual(data, {'a': 1})
