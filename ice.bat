@echo off
:: Get the directory where this BAT file lives
set SCRIPT_DIR=%~dp0

:: Call Python from PATH and run genreq.py inside this same directory
python "%SCRIPT_DIR%genreq.py"