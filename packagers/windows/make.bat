:: pip install pyqt5 requests pypiwin32 setproctitle psutil youtube_dl pyinstaller
@echo off
if not "%1"=="am_admin" (
    powershell -Command "Start-Process -Verb RunAs -FilePath '%0' -ArgumentList 'am_admin'"
    exit /b
)

set pdir=%~dp0
cd %pdir%
cd ../..
@echo on

pyinstaller ".\mounzil\Mounzil.py" -p "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64" -p %USERPROFILE%\AppData\Local\Programs\Python\Python312\Lib\site-packages\PyQt5\Qt5\bin\ -w -F -i %pdir%\mounzil.ico -n "Mounzil" --version-file %pdir%\version.py
copy %pdir%\aria2\64\aria2c.exe dist\aria2c.exe 
copy %pdir%\ffmpeg\64\ffmpeg.exe dist\ffmpeg.exe 

pause