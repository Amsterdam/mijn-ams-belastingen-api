#!/usr/bin/env python3

import json
from sys import argv

from belastingen.api.belastingen.key2belastingen import K2bConnection
from belastingen.config import get_K2B_api_location, get_bearer_token

bsn = argv[1]

connection = K2bConnection(get_K2B_api_location(), get_bearer_token())

raw_data = connection.get_data(bsn)
data = connection._transform(raw_data)

print(json.dumps(raw_data, indent=2, default=str))
print("\n\n----\n\n")
print(json.dumps(data, indent=2, default=str))
