#!/bin/bash

command -v python3 -m venv >/dev/null 2>&1 || { echo >&2 "Python 3.3 required. Install it and try again. Aborting"; exit 1; }

if [ ! -d "env" ]; then
    echo "No virtualenv. Creating one"
    python3 -m venv env
    source env/bin/activate
    if python -m ensurepip; then
        echo "We're under Python 3.4+, no need to try to install pip!"
    else
        python get-pip.py --force-reinstall
    fi
fi

source env/bin/activate

echo "Installing pip requirements"
pip install -r requirements.txt

echo "Bootstrapping complete! You can now configure, run the app with:"
echo ". env/bin/activate && python manage.py runserver"

