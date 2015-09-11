@echo off
set PYTHONHOME=d:\shared\python3
set PYTHONPATH=x:\rokugani
set QTDIR=%PYTHONHOME%\Lib\site-packages\PyQt5
set QT_PLUGIN_PATH=%QTDIR%\plugins
set QML2_IMPORT_PATH=%QTDIR%\qml

set PATH=%PYTHONHOME%;%PYTHONHOME%\Scripts;%QTDIR%;%PATH%

call x:\rokugani\.venv\scripts\activate.bat
