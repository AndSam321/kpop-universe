from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
# Creating function based view
def getRoutes(request):
    routes = [ # Allowing users to see
        'GET /api/',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes) # Using more than just Python dicts.

@api_view(['GET']) # Allowing Get request
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True) # Many is multiple objects, serializer all 
    return Response(serializer.data)

 