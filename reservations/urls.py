from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomListView, ReservationCreateView, ReservationListView
from .views import RoomAdminViewSet, TableAdminViewSet,RoomDetailView,get_table_by_room_and_id

router = DefaultRouter()
router.register('admin/rooms', RoomAdminViewSet)
router.register('admin/tables', TableAdminViewSet)

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:room_id>/tables/<int:table_id>/', get_table_by_room_and_id),

    path('reserve/', ReservationCreateView.as_view(), name='reservation-create'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),
    path('', include(router.urls)),
]
