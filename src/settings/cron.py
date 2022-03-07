from django.core.management import call_command

def mediabackup_():
    try:
        call_command('mediabackup')
    except Exception as e:
        print(e)