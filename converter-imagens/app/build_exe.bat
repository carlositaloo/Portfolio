@echo off
REM Gera o executável com PyInstaller
python -m pip install -r requirements.txt
python -m pip install pyinstaller
pyinstaller --onefile converterHeic.py --name ConverterHEIC
pause
