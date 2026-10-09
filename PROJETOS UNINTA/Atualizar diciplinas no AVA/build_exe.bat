@echo off
echo Gerando executavel...
echo.

pyinstaller --noconfirm ^
    --onefile ^
    --console ^
    --name "AutomacaoEAD" ^
    --add-data "img;img" ^
    "Enviar disciplina EAD.py"

echo.
if %ERRORLEVEL% == 0 (
    echo Executavel gerado com sucesso em: dist\AutomacaoEAD.exe
) else (
    echo Erro ao gerar o executavel. Verifique se o PyInstaller esta instalado:
    echo     pip install pyinstaller
)

echo.
pause
