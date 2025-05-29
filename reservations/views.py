from rest_framework import generics, viewsets
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse, Http404

from .models import Room, Table, Reservation
from .serializers import RoomSerializer, TableSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.prefetch_related('tables').all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # 👈 This allows public access (no auth)
    


# class ReservationCreateView(generics.CreateAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
#     permission_classes = [AllowAny]  # 👈 This allows public access (no auth)
#     def create(self, request, *args, **kwargs):
#         try:
#             return super().create(request, *args, **kwargs)
#         except Exception as e:
#             print(f"🔥 Error in ReservationCreateView: {e}")
#             return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.core.mail import send_mail
from django.conf import settings

class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            reservation = self.get_queryset().get(id=response.data['id'])

            # 1️⃣ Send email to assigned staff
            staff_email = reservation.table.room.assigned_staff_email
            send_mail(
                subject='New Table Reservation Assigned',
                message=f"""
Hello,

You have guests reserved at the following table:

Room: {reservation.table.room.name}
Table: {reservation.table.name}
Guests: {reservation.number_of_guests}
Customer: {reservation.customer_name}
Time: {reservation.start_time.strftime('%Y-%m-%d %H:%M')} to {reservation.end_time.strftime('%Y-%m-%d %H:%M')}

Please be prepared to serve.

Thanks.
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[staff_email],
                fail_silently=False,
            )

            # 2️⃣ Send email to each guest
            guest_emails = reservation.get_email_list()
            if guest_emails:
                send_mail(
                    subject='You are Invited to a Table Reservation',
                    message=f"""
Hello,

You are invited to join a reservation:

Host: {reservation.customer_name}
Room: {reservation.table.room.name}
Table: {reservation.table.name}
Time: {reservation.start_time.strftime('%Y-%m-%d %H:%M')} to {reservation.end_time.strftime('%Y-%m-%d %H:%M')}
Message from Host: {reservation.description or "No message provided."}

We look forward to having you!

Cheers.
""",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=guest_emails,
                    fail_silently=False,
                )

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
    permission_classes = [AllowAny]
# views.py

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













# # views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate
# from rest_framework import status

# class LDAPLoginView(APIView):
#     permission_classes = []

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         user = authenticate(request, username=username, password=password)
#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({"token": token.key})
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status

class LDAPLoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            user_data = {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                # Add other user fields if needed
            }
            return Response({
                "token": token.key,
                "user": user_data
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
