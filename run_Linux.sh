#!/bin/bash

# Chemin du répertoire du script .sh
SCRIPT_PATH=$(dirname "$0")

# Chemin vers les dossiers "utils" et "App" relatifs au répertoire du script
UTILS_PATH="$SCRIPT_PATH/utils"
APP_PATH="$SCRIPT_PATH/App"

# Ajouter les dossiers au PYTHONPATH
export PYTHONPATH="$UTILS_PATH:$APP_PATH:$PYTHONPATH"

# Exécution du code Python
python "$SCRIPT_PATH/App/Main.py"