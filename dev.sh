export FLASK_CONFIG=development
export FLASK_APP=app_main.py

gunicorn --workers 3 --bind 0.0.0.0:5000 app_main:core