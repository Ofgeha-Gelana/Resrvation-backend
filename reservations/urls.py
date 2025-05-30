# # from django.urls import path, include
# # from rest_framework.routers import DefaultRouter
# # from .views import RoomListView, ReservationCreateView, ReservationListView
# # from .views import RoomAdminViewSet, TableAdminViewSet,RoomDetailView,get_table_by_room_and_id

# # router = DefaultRouter()
# # router.register('admin/rooms', RoomAdminViewSet)
# # router.register('admin/tables', TableAdminViewSet)


# # urlpatterns = [
# #     path('rooms/', RoomListView.as_view(), name='room-list'),
# #     path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
# #     path('rooms/<int:room_id>/tables/<int:table_id>/', get_table_by_room_and_id),

# #     path('reserve/', ReservationCreateView.as_view(), name='reservation-create'),
# #     path('reservations/', ReservationListView.as_view(), name='reservation-list'),

# #     path('', include(router.urls)),
# # ]


# # from .views import LDAPLoginView

# # urlpatterns += [
# #     path('api/ldap-login/', LDAPLoginView.as_view(), name='ldap-login'),
# # ]



# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     RoomListView, RoomDetailView, get_table_by_room_and_id,
#     ReservationCreateView, ReservationListView,
#     RoomAdminViewSet, TableAdminViewSet,
#     LDAPLoginView
# )

# router = DefaultRouter()
# router.register('admin/rooms', RoomAdminViewSet)
# router.register('admin/tables', TableAdminViewSet)

# urlpatterns = [
#     path('rooms/', RoomListView.as_view(), name='room-list'),
#     path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
#     path('rooms/<int:room_id>/tables/<int:table_id>/', get_table_by_room_and_id),

#     path('reserve/', ReservationCreateView.as_view(), name='reservation-create'),
#     path('reservations/', ReservationListView.as_view(), name='reservation-list'),


#     path('', include(router.urls)),
# ]

# # urls.py
# from django.urls import path, include
# from .views import LDAPLoginView  # 👈 Import your view

# urlpatterns = [
#     # ... existing paths ...
#     path('auth/ldap-login/', LDAPLoginView.as_view(), name='ldap-login'),
# ]




from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomListView, RoomDetailView, get_table_by_room_and_id,
    ReservationCreateView, ReservationListView,
    RoomAdminViewSet, TableAdminViewSet,
    LDAPLoginView
)

router = DefaultRouter()
router.register('admin/rooms', RoomAdminViewSet)
router.register('admin/tables', TableAdminViewSet)

urlpatterns = [
    # main API routes
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:room_id>/tables/<int:table_id>/', get_table_by_room_and_id),

    path('reserve/', ReservationCreateView.as_view(), name='reservation-create'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),

    # LDAP login endpoint ✅
    path('auth/ldap-login/', LDAPLoginView.as_view(), name='ldap-login'),

    # admin API routes (router)

    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),


]
