# Create `.env` file
```.env
MYSQL_DATABASE_NAME=""
MYSQL_DATABASE_USER=""
MYSQL_DATABASE_PASSWORD=""
MYSQL_DATABASE_HOST="127.0.0.1"
MYSQL_DATABASE_PORT="3306"
MYSQL_DATABASE_TIME_ZONE="Asia/Bangkok"

MDB_DB_NAME="db_Test"
MDB_HOST="127.0.0.1"
MDB_POST="27017"
MDB_USER=""
MDB_PASSWORD=""

SECRET_KEY=''
DEBUG = 'True'
SERVERNAMES= 'localhost 127.0.0.1'

EMAIL_USE_TLS = False
EMAIL_HOST = ""
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = ""
SERVER_EMAIL = ""
```

# Django

## Step to start project
Install requirements
```bash
pip install -r requirements.txt
```

And start Django
```bash
python manage.py runserver
```

## Developer mode
in `settings.py` to set `DEBUG is True`
```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
```

Enable `INTERNAL_IPS` (not necessary)
```python
# For developer mode
INTERNAL_IPS = [
    "127.0.0.1",
]
```

## Productions

in `settings.py` to set `DEBUG is False`
```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
```

Get new staticfiles edited.
```bash
python manage.py collectstatic
```

## Django message
```python
msg = "Must put 'help' in subject when cc'ing yourself."
     self.add_error('username', msg)
     {{form.errors.username}}
```

## django clear migrations files
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -name "*.pyc" -exec rm -f {} \;
```
