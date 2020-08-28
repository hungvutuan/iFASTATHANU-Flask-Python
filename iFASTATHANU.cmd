@echo off
title iFASTATHANU (0.1.0)
set FLASK_APP=app.py
set FLASK_RUN_PORT=5000
set FLASK_RUN_HOST=0.0.0.0
python -m flask run -h 0.0.0.0