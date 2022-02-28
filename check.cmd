@echo off
.\venv\Scripts\pycodestyle.exe zorkweb --ignore=E128,W503
.\venv\Scripts\pylint zorkweb --disable=C