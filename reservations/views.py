from rest_framework import generics, viewsets
from .models import Room, Table, Reservation
from .serializers import RoomSerializer, TableSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticated

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.prefetch_related('tables').all()
    serializer_class = RoomSerializer

class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class RoomAdminViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

class TableAdminViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

class ReservationListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
