import sys
sys.path.append(".")

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pywikigame.settings')

import django
django.setup()

from pywikigame.models import Match, Player

import dwebsocket.websocket

Match.objects.all().delete()
Player.objects.all().delete()
