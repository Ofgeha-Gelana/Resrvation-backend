from django.urls import path
from .views import GetSummaryView

urlpatterns = [
    path("get-summary/", GetSummaryView.as_view(), name="get-summary"),
]
