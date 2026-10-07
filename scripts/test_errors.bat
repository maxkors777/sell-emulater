@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo == script with unknown command ==
python emulater.py --vfs vfs_root --script scripts\start_error.txt
echo exit code: %ERRORLEVEL%
echo == script with bad arguments ==
python emulater.py --vfs vfs_root --script scripts\start_bad_args.txt
echo exit code: %ERRORLEVEL%
echo == missing script ==
python emulater.py --script scripts\no_such_file.txt
echo exit code: %ERRORLEVEL%
echo == missing VFS, expect code 2 ==
python emulater.py --vfs C:\no\such\vfs
echo exit code: %ERRORLEVEL%
echo == unknown option, expect code 2 ==
python emulater.py --bogus
echo exit code: %ERRORLEVEL%
echo == option without value, expect code 2 ==
python emulater.py --vfs
echo exit code: %ERRORLEVEL%
pause
