import requests


class K2bConnection:
    """ Class to manage the connection to Key2Belastingen. """
    def __init__(self):
        pass

    def get_data(self, bsn):
        return requests.get('')

    def get_stuff(self, bsn):
        """ Get the things from the API. """
        return self.get_data(bsn)
        pass
