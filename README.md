# django-tailwindcss
Django template using Tailwindcss.

## Step to start project
Install requirements
```bash
pip install -r requirements.txt
```

Install Tailwind & node_modules & Set staticfile(Because Run Product)
```bash
python manage.py tailwind install --no-input;
python manage.py tailwind build --no-input;
python manage.py collectstatic --no-input;
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

Start Tailwind
```bash
python manage.py tailwind start
```

## Productions

in `settings.py` to set `DEBUG is False`
```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
```

Disable `INTERNAL_IPS` (not necessary)
```python
# For developer mode
#INTERNAL_IPS = [
#    "127.0.0.1",
#]
```

Build Taiwind to productions.
```bash
python manage.py tailwind build
```

Get new staticfiles edited.
```bash
python manage.py collectstatic
```

   msg = "Must put 'help' in subject when cc'ing yourself."
            self.add_error('username', msg)
            {{form.errors.username}}


find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -name "*.pyc" -exec rm -f {} \;
