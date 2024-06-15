@echo off

REM Activate the Python virtual environment
call .\venv\Scripts\activate.bat

REM Execute randomMidi.py
python daslightMidi.py

REM Deactivate the virtual environment
call .\venv\Scripts\deactivate.bat
