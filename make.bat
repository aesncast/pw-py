@echo off

REM set the date correctly before building
python3 pw\config.py
pyinstaller -i images\icon.ico --onefile --console pw\__main__.py -n pw-py
