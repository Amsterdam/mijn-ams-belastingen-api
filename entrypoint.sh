#!/bin/sh
# BSN_TRANSLATIONS is an encrypted value provided by deployment
mkdir -p /files/bsn_translations
echo "${BSN_TRANSLATIONS}" > /files/bsn_translations/bsn_translations.json
uwsgi --ini /app/uwsgi.ini
