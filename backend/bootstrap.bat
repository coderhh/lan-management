@echo off
set FLASK_APP=./src/main.py
set FLASK_ENV=development
python -m flask run -h 0.0.0.0