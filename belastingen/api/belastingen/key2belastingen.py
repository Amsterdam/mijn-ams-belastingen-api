import requests


class K2bConnection:
    """ Class to manage the connection to Key2Belastingen. """
    def __init__(self, api_location):
        self.api_location = api_location

    def get_data(self, bsn: str):
        url = "%s?subjid=%s" % (self.api_location, bsn)
        response = requests.get(url)
        return response.json()

    def _transform(self, message):
        res = {
            "tips": [
            ],
            "meldingen": [

            ],
            "isKnown": False
        }

        if message["status"] == "BSN known":
            res['isKnown'] = True

        for i in message["data"]:
            if i['categorie'] == 'F2':
                # ignore this one for now
                pass

            elif i['categorie'] == 'M1':
                # melding
                new_melding = {
                    "id": i["nummer"],
                    "priority": i["prioriteit"],
                    "datePublished": i["datum"],
                    "title": i["titel"],
                    "description": i["omschrijving"],
                    "url": {
                        "title": i["url_naam"],
                        "url": i["url"],
                    }
                }
                res["meldingen"].append(new_melding)

            elif i['categorie'] == 'M2':
                new_tip = {
                    "id": i["nummer"],
                    "priority": i["prioriteit"],
                    "datePublished": i["datum"],
                    "title": i["titel"],
                    "description": i["omschrijving"],
                    "url": {
                        "title": i["url_naam"],
                        "url": i["url"],
                    }
                }
                res["tips"].append(new_tip)

        return res

    def get_stuff(self, bsn: str):
        """ Get the things from the API. """
        json_data = self.get_data(bsn)
        return self._transform(json_data)
