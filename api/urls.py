from django.urls import path
from api import views

urlpatterns = [
    # Class Attendance Enpoints
    path('classes/', views.ClassAttendanceView.as_view()),
    path('classes/attendance/by-class/', views.FetchClassAttendanceByClassNameView.as_view()),
    path('classes/attendance/by-workspace/', views.FetchClassAttendanceByWorkspaceView.as_view()),

    # Bus Attendance Endpoints
    path('buses/', views.BusAttendanceView.as_view()),
    path('buses/attendance/by-bus/', views.FetchBusAttendanceByBusNameView.as_view()),
    path('buses/attendance/by-workspace/', views.FetchBusAttendanceByWorkspaceView.as_view()),
]