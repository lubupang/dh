@echo off
start /min cmd /c pip install Crypto -i https://pypi.doubanio.com/simple
start /min cmd /c python "%~dp0/ui.py" %*