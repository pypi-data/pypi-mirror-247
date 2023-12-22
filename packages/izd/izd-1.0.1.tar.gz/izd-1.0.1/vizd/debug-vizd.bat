@echo off
python3 vizd.pyw %*
echo %cmdcmdline% | find /i "%~0" >nul && pause
