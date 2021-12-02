@echo off

echo Checking python installation
echo.

python --version 3>NUL
if errorlevel 1 goto NoPython

echo.
echo Python is installed

py -m pip install urllib3 asyncio yt-dlp discord.py[voice] validators

echo.
echo Dependencies successfully installed...
pause

goto:eof

:NoPython
echo.
echo Python not installed
echo Installing python3.9

cd install
python.exe

py -m pip install urllib3 asyncio yt-dlp discord.py[voice] validators

echo.
echo Dependencies successfully installed...
pause