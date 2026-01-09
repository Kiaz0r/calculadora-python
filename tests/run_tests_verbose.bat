@echo off
setlocal

cd /d "%~dp0"

cd ..

if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
)

python -m unittest discover -s tests -p "test_*.py" -v

if %ERRORLEVEL% EQU 0 (
    echo(
    echo Tests OK ^(exit code %ERRORLEVEL%^)
) else (
    echo(
    echo Tests falharam ^(exit code %ERRORLEVEL%^)
    pause
)

exit /b %ERRORLEVEL%
