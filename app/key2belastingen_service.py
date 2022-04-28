import requests

from app.config import get_bsn_translations


class K2bConnection:
    """Class to manage the connection to Key2Belastingen."""

    def __init__(self, api_location, bearer_token):
        self.api_location = api_location
        self.bearer_token = bearer_token

    def _translate_bsn(self, bsn):
        """Use a translation table to be able to test in acc."""
        translation_table = get_bsn_translations()
        if bsn in translation_table:
            return translation_table[bsn]
        else:
            return bsn

    def get_data(self, bsn: str):
        bsn = self._translate_bsn(bsn)
        url = self.api_location
        headers = {
            "Authorization": "Bearer %s" % self.bearer_token,
            "subjid": bsn,
        }
        response = requests.get(
            url, verify="/etc/ssl/certs/ca-certificates.crt", headers=headers, timeout=9
        )

        response.raise_for_status()

        return response.json()

    def _transform(self, message):
        res = {"tips": [], "meldingen": [], "isKnown": False}

        if message["status"] == "BSN known":
            res["isKnown"] = True

        for i in message["data"]:
            if i["categorie"] == "F2":
                # ignore this one for now
                pass

            elif i["categorie"] == "M1":
                # melding
                new_melding = {
                    "id": f'belasting-{i["nummer"]}',
                    "priority": i["prioriteit"],
                    "datePublished": i["datum"],
                    "title": i["titel"],
                    "description": i["omschrijving"],
                    "link": {
                        "title": i["url_naam"],
                        "to": i["url"],
                    },
                }
                res["meldingen"].append(new_melding)

            elif i["categorie"] == "M2":
                new_tip = {
                    "id": f'belasting-{i["nummer"]}',
                    "priority": i["prioriteit"],
                    "datePublished": i["datum"],
                    "title": i["titel"],
                    "description": i["omschrijving"],
                    "reason": i.get("informatie"),
                    "link": {
                        "title": i["url_naam"],
                        "to": i["url"],
                    },
                }
                res["tips"].append(new_tip)

        return res

    def get_stuff(self, bsn: str):
        """Get the things from the API."""
        json_data = self.get_data(bsn)
        return self._transform(json_data)
