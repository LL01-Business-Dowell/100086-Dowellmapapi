from django.urls import re_path
from api import views

urlpatterns = [
    # Class Attendance Enpoints
    re_path(r'^classes$', views.ClassAttendanceView.as_view()),
    re_path(r'^classes/attendance/by-class$', views.FetchClassAttendanceByClassNameView.as_view()),
    re_path(r'^classes/attendance/by-workspace$', views.FetchClassAttendanceByWorkspaceView.as_view()),

    # Bus Attendance Endpoints
    re_path(r'^buses$', views.BusAttendanceView.as_view()),
    re_path(r'^buses/attendance/by-bus$', views.FetchBusAttendanceByBusNameView.as_view()),
    re_path(r'^buses/attendance/by-workspace$', views.FetchBusAttendanceByWorkspaceView.as_view()),
]