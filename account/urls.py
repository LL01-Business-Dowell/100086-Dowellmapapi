from django.urls import path

from .views import *

urlpatterns = [
    path("test/", index, name="index"),
    path("user-management/",UserManagement.as_view()),
    path("kiosk/",KioskAPIView.as_view()),

]