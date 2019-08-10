export FLASK_CONFIG=development
export FLASK_APP=app_main.py

# recommend worker = (2 * CPU) + 1

gunicorn --workers=3 --threads=3 --bind 0.0.0.0:4000 app_main:core