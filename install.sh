virtualenv -p python3 venv;
. venv/Scripts/activate;
pip3 install -r requirements.txt;
pre-commit install;