from rest_framework import generics, viewsets
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse, Http404

from .models import Room, Table, Reservation
from .serializers import RoomSerializer, TableSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.prefetch_related('tables').all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # 👈 This allows public access (no auth)


class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]  # 👈 This allows public access (no auth)
    # def create(self, request, *args, **kwargs):
    #     try:
    #         return super().create(request, *args, **kwargs)
    #     except Exception as e:
    #         print(f"🔥 Error in ReservationCreateView: {e}")
    #         return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RoomAdminViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        print("DEBUG: Token or user:", request.user)  # Check user
        print("DEBUG: Headers:", request.headers)  # Check headers
        return super().create(request, *args, **kwargs)
class RoomDetailView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # 👈 This allows public access (no auth)

class TableAdminViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # 🔥 Required for FormData/file uploads

    def create(self, request, *args, **kwargs):
        print("DEBUG: Token or user:", request.user)  # Check user
        print("DEBUG: Headers:", request.headers)  # Check headers
        return super().create(request, *args, **kwargs)
class ReservationListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]  # 👈 This allows public access (no auth)

# views.py
class ReservationDetailView(RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny] 
def get_table_by_room_and_id(request, room_id, table_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404("Room not found")

    try:
        table = room.tables.get(id=table_id)  # Uses related_name='tables'
    except Table.DoesNotExist:
        raise Http404("Table not found in this room")

    data={
        "room": {
            "id": room.id,
            "name": room.name,
            "address": room.address,
            "assigned_staff_email": room.assigned_staff_email,
            "number_of_tables": room.number_of_tables,
        },
        "table": {
            "id": table.id,
            "name": table.name,
            "capacity": table.capacity,
            "image": request.build_absolute_uri(table.image.url) if table.image else None,
            "amenities": table.amenities,

        }
    }

    return JsonResponse(data)
