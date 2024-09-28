"""
Context processor for adding public rooms to base templates
"""
from .models import Room


def public_rooms(request):
    rooms = Room.objects.all()
    return {'rooms': rooms}