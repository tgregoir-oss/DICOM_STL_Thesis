@echo off
setlocal

REM Chemin du répertoire du script .bat
set "SCRIPT_PATH=%~dp0"

REM Chemin vers les dossiers "utils" et "App" relatifs au répertoire du script
set "UTILS_PATH="%SCRIPT_PATH%utils""
set "APP_PATH="%SCRIPT_PATH%App""

REM Ajouter les dossiers au PYTHONPATH
set "PYTHONPATH=%UTILS_PATH%;%APP_PATH%;%PYTHONPATH%"

REM Exécution du code Python
start "" python "%SCRIPT_PATH%App\Main.py"

endlocal
