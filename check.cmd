@echo off
.\venv\Scripts\pycodestyle.exe Zork.py --ignore=E128,W503
.\venv\Scripts\pylint Zork.py --disable=C