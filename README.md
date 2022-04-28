# Mijn Amsterdam belastingen API

## Introduction

A REST API which discloses the Amsterdam Belastingen data

### Local development

1. Clone repo and `cd` in
2. Create a virtual env and activate
3. Run `pip install -r requirements.txt`
4. Set environment variables:
   - `export FLASK_APP=app/server.py`
    
5. Run `flask run`
6. `curl http://localhost:5000/status/health` to see if api is up-and-running

### Testing
In your env created for Local development

1. Run `python -m unittest`
