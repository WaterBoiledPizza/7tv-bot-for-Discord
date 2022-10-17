@echo off
python.exe -m pip install --upgrade pip --user
python.exe -m pip install -r requirements.txt %* --user
pause
