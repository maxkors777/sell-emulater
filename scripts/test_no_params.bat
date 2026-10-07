@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo == no parameters ==
python emulater.py
echo exit code: %ERRORLEVEL%
pause
