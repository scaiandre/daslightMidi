@echo off

python -m venv venv

REM Activate the Python virtual environment
call .\venv\Scripts\activate.bat

pip install keyboard mido python-rtmidi

REM Deactivate the virtual environment
call .\venv\Scripts\deactivate.bat