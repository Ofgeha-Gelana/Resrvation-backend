from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomListView, ReservationCreateView, ReservationListView
from .views import RoomAdminViewSet, TableAdminViewSet

router = DefaultRouter()
router.register('admin/rooms', RoomAdminViewSet)
router.register('admin/tables', TableAdminViewSet)

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('reserve/', ReservationCreateView.as_view(), name='reservation-create'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),
    path('', include(router.urls)),
]
