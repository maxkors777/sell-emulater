@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo == --vfs + --script (ok script) ==
python emulater.py --vfs vfs_root --script scripts\start_ok.txt
echo exit code: %ERRORLEVEL%
echo == only --vfs (close the window) ==
python emulater.py --vfs vfs_root
echo exit code: %ERRORLEVEL%
echo == only --script (close the window) ==
python emulater.py --script scripts\start_ok.txt
echo exit code: %ERRORLEVEL%
pause
