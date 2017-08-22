# Favicon Finder

## tldr;

Main files:

- favicons/models.py
    - Contains logic for extracting favicon URL from a given URL (see get_favicon_for_url).
- favicons/forms.py
    - Cleans, formats, and validates a given URL to examine.
    - Calls get_favicon_for_url, and creates or modifies a Favicon record on save.
- favicons/management/commands/seed_db.py
    - Provides command for seeding the database (200,000 rows by default)
    - E.g. to process 10 rows, run: python manage.py seed_db 10
- UI Files:
    - favicons/views.py
    - favicons/templates/fav_finder.html
    - favicons/static/favicons/style.css

## Getting started!

```
# clone repo
git clone https://github.com/emanoppo/fav_finder.git

# from your project folder, create local virtual environment
virtualenv fav_finder

# go into virtual environment
cd fav_finder
source bin/activate

# install required python packages
pip install -r requirements.txt

# set up local PostGreSQL database, user, and grant rights
psql
CREATE USER favfinderuser PASSWORD 'yay!';
CREATE DATABASE fav_finder;
CREATE SCHEMA fav_finder;
GRANT ALL ON SCHEMA fav_finder TO favfinderuser;
GRANT ALL ON ALL TABLES IN SCHEMA fav_finder TO favfinderuser;

# run data migrations
python manage.py migrate
```

## Running the app locally!

```
python manage.py runserver

open http://127.0.0.1:8000
```

## Seeding the database!

```
# By default, will process 200,000 rows.
python manage.py seed_db

# Or, specify how many rows to process.
# python manage.py seed_db 5
```
