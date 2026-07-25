import os
import sys
from pathlib import Path
import django
from django.test import Client

# Ensure project src directory is on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_shop.settings')
django.setup()
from django.conf import settings
# Ensure test client host is allowed
settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver', '127.0.0.1', 'localhost']

client = Client()
from django.contrib.sites.models import Site
# Ensure a Site exists for testserver
Site.objects.update_or_create(id=1, defaults={'domain': 'testserver', 'name': 'testserver'})

resp = client.get('/accounts/login/')
print('STATUS:', resp.status_code)
if resp.status_code in (301, 302):
    print('LOCATION:', resp['Location'])
if resp.status_code == 200:
    print('CONTENT_SNIPPET:\n', resp.content.decode()[:800])
else:
    print('BODY_SNIPPET:\n', resp.content.decode()[:800])
