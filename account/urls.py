from django.urls import path

from .views import *

urlpatterns = [
    path("test/", index, name="index"),
    path("user-management/",UserManagement.as_view()),
    path("kiosk/",KioskAPIView.as_view()),
    path("create-database/", create_database_view, name="create_database"),
    path("add-collection/", add_collection_view, name="add_collection")
    
]
