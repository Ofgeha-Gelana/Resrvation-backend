from rest_framework import generics, viewsets
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse, Http404

from .models import Room, Table, Reservation
from .serializers import RoomSerializer, TableSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import localtime
from django.core.mail import send_mail
from django.conf import settings


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.prefetch_related('tables').all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # 👈 This allows public access (no auth)




class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            # Create the reservation
            response = super().create(request, *args, **kwargs)
            reservation = self.get_queryset().get(id=response.data['id'])

            # Send email to assigned staff
            try:
                staff_email = reservation.table.room.assigned_staff_email

                html_content = render_to_string('email/reservation_email.html', {
                    'room': reservation.table.room.name,
                    'table': reservation.table.name,
                    'guests': reservation.number_of_guests,
                    'refreshments': reservation.refreshments or "None",
                    'customer': reservation.customer_name,
                    'start_time': localtime(reservation.start_time).strftime('%Y-%m-%d %I:%M %p'),
                    'end_time': localtime(reservation.end_time).strftime('%Y-%m-%d %I:%M %p'),
                })

                email = EmailMultiAlternatives(
                    subject='New Table Reservation Assigned',
                    body='A new table reservation has been assigned.',
                    from_email=settings.EMAIL_HOST_USER,
                    to=[staff_email],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
            except Exception as e:
                print(f"⚠️ Failed to send staff email: {e}")

            # Send email to guests
            try:
                guest_emails = reservation.get_email_list()
                if guest_emails:
                    html_guest_content = render_to_string('email/guest_invitation_email.html', {
                        'host': reservation.customer_name,
                        'host_email': reservation.email,
                        'location': reservation.table.room.address,
                        'room': reservation.table.room.name,
                        'table': reservation.table.name,
                        'start_time': localtime(reservation.start_time).strftime('%Y-%m-%d %I:%M %p'),
                        'end_time': localtime(reservation.end_time).strftime('%Y-%m-%d %I:%M %p'),
                        'description': reservation.description or "No message provided.",
                    })

                    guest_email_message = EmailMultiAlternatives(
                        subject='You are Invited to a Table Reservation',
                        body='You are invited to a reservation.',
                        from_email=settings.EMAIL_HOST_USER,
                        to=guest_emails,
                    )
                    guest_email_message.attach_alternative(html_guest_content, "text/html")
                    guest_email_message.send()
            except Exception as e:
                print(f"⚠️ Failed to send guest emails: {e}")

            return response

        except Exception as e:
            print(f"🔥 Error in ReservationCreateView: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
