#!/bin/bash
# BSN_TRANSLATIONS is an encrypted value provided by deployment
mkdir -p /files/bsn_translations

# Because ansible ENV forces quotes around JSON values, we have to remove
# them here, first line removes beginning quote and second removes end quote
B=${BSN_TRANSLATIONS#"'"}
echo ${B%"'"} > /files/bsn_translations/bsn_translations.json
uwsgi --ini /api/uwsgi.ini
