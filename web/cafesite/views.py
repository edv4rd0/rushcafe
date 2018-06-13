from django.conf import settings
from importlib import import_module
from django.shortcuts import render

engine = import_module(settings.SESSION_ENGINE)
SessionStore = engine.SessionStore


def frontend(request):
    """This is only to allow easy
    session persistance with Django websocket channels"""
    if not request.session.session_key:
        request.session = SessionStore()
        request.session.create()

    return render(request, 'frontend.html')
