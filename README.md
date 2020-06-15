# block_model_viewer_tracing
Tracing app for block model viewer

# Python

python3 -m venv venv
. venv/bin/activate

pip install Flask
pip install Flask-Heroku
pip install SQLAlchemy
pip install Flask-SQLAlchemy
pip install Psycopg2
pip install gunicorn

# Heroku

heroku login
heroku create
git push heroku master