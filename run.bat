@echo off
rem Run emulater: run.bat [--vfs PATH] [--script FILE]
rem Run tests:    run.bat test
cd /d "%~dp0"
if "%1"=="test" (
    python -m unittest discover -s tests -t . -v
) else (
    python emulater.py %*
)
