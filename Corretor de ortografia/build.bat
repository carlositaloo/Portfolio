@echo off
chcp 65001 > nul
echo.
echo =======================================
echo   Build: Corretor Ortografico
echo =======================================
echo.

echo [1/3] Instalando dependencias...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO: falha ao instalar dependencias.
    pause
    exit /b 1
)

echo.
echo [2/3] Instalando PyInstaller...
pip install pyinstaller
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO: falha ao instalar PyInstaller.
    pause
    exit /b 1
)

echo.
echo [3/3] Gerando executavel...
pyinstaller --onefile --noconsole --name "CorretorOrtografico" --hidden-import=pystray._win32 corretor.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO: falha ao gerar o executavel.
    pause
    exit /b 1
)

echo.
echo =======================================
echo   Pronto!
echo   Executavel gerado em: dist\CorretorOrtografico.exe
echo.
echo   IMPORTANTE: execute o .exe como Administrador
echo   para que a captura global de teclado funcione.
echo =======================================
echo.
pause
